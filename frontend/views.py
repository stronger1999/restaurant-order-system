from decimal import Decimal
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from restaurant.models import MenuItem, RestaurantTable
from orders.models import Order, OrderItem
from payments.models import Payment
from payments.tasks import send_payment_notification


def _cart(request):
    return request.session.setdefault('cart', {})


def home(request):
    featured_items = MenuItem.objects.filter(is_available=True)[:6]

    return render(request, 'frontend/home.html', {
        'featured_items': featured_items
    })


def menu(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    items = (
        MenuItem.objects
        .select_related('category')
        .filter(is_available=True)
    )

    if query:
        items = items.filter(name__icontains=query)

    if category:
        items = items.filter(category__name__iexact=category)

    items = items.order_by('category__name', 'name')

    categories = (
        MenuItem.objects
        .filter(is_available=True)
        .select_related('category')
        .values_list('category__name', flat=True)
        .distinct()
        .order_by('category__name')
    )

    return render(request, 'frontend/menu.html', {
        'items': items,
        'categories': categories,
        'query': query,
        'selected_category': category,
    })
def product_details(request, item_id):

    item = get_object_or_404(
        MenuItem,
        id=item_id,
        is_available=True
    )

    related_items = (
        MenuItem.objects
        .filter(
            category=item.category,
            is_available=True
        )
        .exclude(id=item.id)
        .order_by('?')[:4]
    )

    return render(request, 'frontend/product_details.html', {
        'item': item,
        'related_items': related_items,
    })

@require_POST
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id, is_available=True)

    cart = _cart(request)
    key = str(item.id)

    cart[key] = cart.get(key, 0) + 1

    request.session.modified = True

    messages.success(request, f'{item.name} added to cart.')

    return redirect('cart')


@require_POST
def increase_quantity(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id, is_available=True)

    cart = _cart(request)
    key = str(item.id)

    cart[key] = cart.get(key, 0) + 1

    request.session.modified = True

    return redirect('cart')


@require_POST
def decrease_quantity(request, item_id):
    cart = _cart(request)
    key = str(item_id)

    if key in cart:
        cart[key] = int(cart[key]) - 1

        if cart[key] <= 0:
            del cart[key]

    request.session.modified = True

    return redirect('cart')


@require_POST
def remove_from_cart(request, item_id):
    cart = _cart(request)

    cart.pop(str(item_id), None)

    request.session.modified = True

    return redirect('cart')


def cart(request):
    cart_data = _cart(request)

    ids = [int(i) for i in cart_data.keys()]

    items = MenuItem.objects.filter(id__in=ids)

    lines = []
    total = Decimal('0.00')

    for item in items:
        qty = int(cart_data[str(item.id)])
        line_total = item.price * qty
        total += line_total

        lines.append({
            'item': item,
            'quantity': qty,
            'line_total': line_total,
        })

    return render(request, 'frontend/cart.html', {
        'lines': lines,
        'total': total,
    })


@login_required(login_url='customer_login')
def checkout(request):
    cart_data = _cart(request)

    if not cart_data:
        messages.warning(request, 'Your cart is empty.')
        return redirect('menu')

    if request.method == 'POST':
        table_id = request.POST.get('table') or None
        payment_method = request.POST.get('payment_method', 'OFFLINE')
        notes = request.POST.get('notes', '')

        table = (
            RestaurantTable.objects
            .filter(id=table_id)
            .first()
            if table_id
            else None
        )

        order = Order.objects.create(
            customer=request.user,
            table=table,
            status='PENDING',
            notes=notes
        )

        total = Decimal('0.00')

        items = MenuItem.objects.filter(
            id__in=[int(i) for i in cart_data.keys()]
        )

        for item in items:
            qty = int(cart_data[str(item.id)])

            OrderItem.objects.create(
                order=order,
                menu_item=item,
                quantity=qty,
                unit_price=item.price
            )

            total += item.price * qty

        if payment_method == 'ONLINE':
            blik_code = request.POST.get('blik_code', '').strip()

            if not blik_code.isdigit() or len(blik_code) != 6:
                payment = Payment.objects.create(
                    order=order,
                    method='ONLINE',
                    status='FAILED',
                    amount=total,
                    transaction_reference='BLIK-INVALID',
                    failure_reason='Invalid BLIK code'
                )

                order.status = 'REJECTED'
                order.save()

                send_payment_notification.delay(payment.id, payment.status)

                request.session['cart'] = {}

                messages.error(request, 'Order rejected: invalid BLIK code.')

                return redirect('my_orders')

            success_codes = ['111111', '222222', '333333']
            failed_codes = ['999999', '888888', '777777']

            if blik_code in success_codes:
                payment_status = 'APPROVED'
            elif blik_code in failed_codes:
                payment_status = 'FAILED'
            else:
                payment_status = (
                    'FAILED'
                    if random.random() < 0.3
                    else 'APPROVED'
                )

            payment = Payment.objects.create(
                order=order,
                method='ONLINE',
                status=payment_status,
                amount=total,
                transaction_reference=f'BLIK-{blik_code}',
                failure_reason=(
                    'Sandbox rejected BLIK payment'
                    if payment_status == 'FAILED'
                    else ''
                )
            )

            if payment_status == 'FAILED':
                order.status = 'REJECTED'

                messages.error(
                    request,
                    f'Order #{order.id} rejected because payment failed.'
                )
            else:
                order.status = 'SUBMITTED'

                messages.success(
                    request,
                    f'Order #{order.id} created successfully.'
                )

            order.save()

            send_payment_notification.delay(payment.id, payment.status)

        else:
            payment = Payment.objects.create(
                order=order,
                method='OFFLINE',
                status='PENDING',
                amount=total
            )

            order.status = 'SUBMITTED'
            order.save()

            send_payment_notification.delay(payment.id, payment.status)

            messages.info(
                request,
                'Offline payment request created. Waiting for admin approval.'
            )

        request.session['cart'] = {}

        return redirect('my_orders')

    tables = RestaurantTable.objects.filter(is_active=True).order_by('number')

    return render(request, 'frontend/checkout.html', {
        'tables': tables
    })


@login_required(login_url='customer_login')
def my_orders(request):
    orders = (
        Order.objects
        .filter(customer=request.user)
        .prefetch_related('items__menu_item', 'payments')
        .order_by('-created_at')
    )

    return render(request, 'frontend/my_orders.html', {
        'orders': orders
    })


def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('menu')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'frontend/login.html')


def customer_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(
                request,
                user,
                backend='django.contrib.auth.backends.ModelBackend'
            )

            return redirect('menu')

    else:
        form = UserCreationForm()

    return render(request, 'frontend/register.html', {
        'form': form
    })


@login_required(login_url='customer_login')
def customer_logout(request):
    logout(request)

    return redirect('home')