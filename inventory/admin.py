from django.contrib import admin
from .models import Profile,Product,Customer,Bill,BillItem

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Bill)
admin.site.register(BillItem)

