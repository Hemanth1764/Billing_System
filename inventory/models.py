from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES=(
        ('admin','Admin'),
        ('cashier','Cashier'),
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=10,choices=ROLE_CHOICES,default='cashier')

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# Ensure every user has a Profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

class Product(models.Model):
    name=models.CharField(max_length=200,unique=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveBigIntegerField(default=0)
    low_stock_threshold=models.PositiveIntegerField(default=5)

    def __str__(self):
        return f"{self.name} - {self.quantity} left"
    
    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold
    
class Customer(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(blank=True,null=True)
    phone=models.CharField(max_length=15,blank=True,null=True)

    def __str__(self):
        return self.name
    
class Bill(models.Model):
    customer= models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True, blank=True)
    cashier=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="bills")
    created_at=models.DateTimeField(auto_now_add=True)
    total_amount=models.DecimalField(max_digits=12,decimal_places=2,default=0)

    def __str__(self):
        return f"Bill #{self.id} - {self.created_at.date()}"
    
class BillItem(models.Model):
    bill=models.ForeignKey(Bill,on_delete=models.CASCADE,related_name="items")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    price= models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def subtotal(self):
        return self.quantity * self.price
    