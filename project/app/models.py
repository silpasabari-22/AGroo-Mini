from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Customuser(AbstractUser):
    users = models.CharField(max_length=100)
    adress = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)


    def __str__(self):
        return self.username



class Product(models.Model):
    farmer_id=models.ForeignKey(Customuser,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    product_category=models.CharField(max_length=100)
    product_image=models.ImageField()
    quantity=models.IntegerField()
    price=models.IntegerField()

    def __str__(self):
        return self.product_name



class Cart(models.Model):
    user_id=models.ForeignKey(Customuser,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.IntegerField(default=0)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f"Cart of {self.user_id.username}"
    



class DeliveryAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)

    # Address fields
    house_no = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    # Optional fields
    landmark = models.CharField(max_length=255, blank=True, null=True)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} - {self.city}"
    


class Order(models.Model):
    user_id = models.ForeignKey(Customuser, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"Order {self.id} by {self.user_id.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total(self):
        return self.quantity * self.price

    