from django.contrib import admin
from .models import Seller

# Register your models here.
class SellerModelAdmin(admin.ModelAdmin):
    list_display = ('id','user','first_name','last_name','mobile_no','gender','product_category','country','state','city','bank_name','account_no','gst_no','email_verified')
admin.site.register(Seller,SellerModelAdmin)
