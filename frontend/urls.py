from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path('', views.home, name='home'),

    # MENU
    path('menu/', views.menu, name='menu'),

    # PRODUCT DETAILS
    path(
        'menu/item/<int:item_id>/',
        views.product_details,
        name='product_details'
    ),

    # CART
    path('cart/', views.cart, name='cart'),

    path(
        'cart/add/<int:item_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/remove/<int:item_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    # QUANTITY CONTROLS
    path(
        'cart/increase/<int:item_id>/',
        views.increase_quantity,
        name='increase_quantity'
    ),

    path(
        'cart/decrease/<int:item_id>/',
        views.decrease_quantity,
        name='decrease_quantity'
    ),

    # CHECKOUT
    path('checkout/', views.checkout, name='checkout'),

    # ORDERS
    path('orders/', views.my_orders, name='my_orders'),

    # AUTH
    path('login/', views.customer_login, name='customer_login'),

    path(
        'register/',
        views.customer_register,
        name='customer_register'
    ),

    path(
        'logout/',
        views.customer_logout,
        name='customer_logout'
    ),
]