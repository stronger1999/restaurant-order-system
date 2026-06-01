from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from restaurant.models import RestaurantTable, MenuCategory, MenuItem

class Command(BaseCommand):
    help = 'Seed demo data'
    def handle(self, *args, **kwargs):
        User.objects.get_or_create(username='admin', defaults={'is_staff': True, 'is_superuser': True, 'email':'admin@example.com'})
        admin = User.objects.get(username='admin'); admin.set_password('adminpass'); admin.is_staff=True; admin.is_superuser=True; admin.save()
        for n in range(1,6): RestaurantTable.objects.get_or_create(number=n, defaults={'seats':4})
        cat,_ = MenuCategory.objects.get_or_create(name='Main Dishes')
        MenuItem.objects.get_or_create(category=cat, name='Chicken Burger', defaults={'price':'29.99','description':'Burger with fries'})
        MenuItem.objects.get_or_create(category=cat, name='Pasta Alfredo', defaults={'price':'34.99','description':'Cream sauce pasta'})
        self.stdout.write(self.style.SUCCESS('Demo data created. Admin: admin / adminpass'))
