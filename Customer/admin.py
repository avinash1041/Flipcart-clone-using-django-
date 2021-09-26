from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.
from django.contrib import admin
from .models import *

# Register your models here.
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ('id','user','first_name','last_name','gender','country','state','city','area_name','street_name','house_no','email_verified')
admin.site.register(Customer,CustomerModelAdmin)

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('id','title','price','discout_price','description','brand','category','product_img')
admin.site.register(Product,ProductModelAdmin)

class CartModelAdmin(admin.ModelAdmin):
    list_display = ('id','user','product','quantity')
admin.site.register(Cart,CartModelAdmin)


@admin.register(OrderPlaces)
class OrderPlacesModelAdmin(admin.ModelAdmin):
    list_display = ('id','user','customer','customer_info','product','product_info','quantity','order_date','status')


    def customer_info(self,obj):
        link = reverse('admin:Customer_customer_change',args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.first_name)

    def product_info(self,obj):
        link = reverse('admin:Customer_product_change',args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ('user','amount','payment_id','paid')
admin.site.register(Payment,PaymentModelAdmin)

