from django.db import models
from listings.models import Product
from django.conf import settings
from django.urls import reverse

ORDER_STATUS = [
    ('Created', 'Created'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Ready for pickup', 'Ready for pickup'),
    ('Completed', 'Completed')
]

TRANSPORT_CHOICES = [
    ('Courier delivery', 'Courier delivery'), 
    ('Recipient pickup', 'Recipient pickup')
]

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        blank=True, 
        null=True
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, 
                            default='Created')
    note = models.TextField(blank=True)
    transport = models.CharField(max_length=20, choices=TRANSPORT_CHOICES)
    transport_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order #{self.id}'

    def get_absolute_url(self):
        return reverse(
            'orders:order_detail',
            args=[self.id]
        )

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        total_cost += self.transport_cost
        return total_cost

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
