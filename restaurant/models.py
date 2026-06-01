from django.db import models

class RestaurantTable(models.Model):
    number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField(default=4)
    is_active = models.BooleanField(default=True)
    def __str__(self): return f"Table {self.number}"

class MenuCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class MenuItem(models.Model):

    category = models.ForeignKey(
        MenuCategory,
        on_delete=models.PROTECT,
        related_name='items'
    )

    name = models.CharField(max_length=120)

    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to='menu_items/',
        blank=True,
        null=True
    )

    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('category','name')

    def __str__(self):
        return self.name
