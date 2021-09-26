import random

import val as val
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max, Min
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import *
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.shortcuts import redirect,render
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .tokens import account_activation_token





def  homeview(request):
    Mobile = Product.objects.filter(category='Mobile')
    laptop = Product.objects.filter(category='Laptop')
    Shoesdata = Product.objects.filter(category='Shoes')
    topwear = Product.objects.filter(category='Top Wear')
    bottomwear = Product.objects.filter(category='Bottom Wear')
    home = Product.objects.filter(category='HK')
    Books = Product.objects.filter(category='Books')
    Musical = Product.objects.filter(category='Musical Instruments')
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    template_name = 'Customer/home.html'
    context = {'Mobile':Mobile, 'Shoesdata':Shoesdata, 'laptop':laptop, 'topwear':topwear,
               'bottomwear':bottomwear,'home':home,'Musical':Musical,
               'Books':Books,'total_item':total_item}
    return render(request,template_name,context)



def  search(request):
    if 'q' in request.GET:
        q=request.GET['q']
        data = Product.objects.filter(Q(title__icontains=q) | Q(brand__icontains=q) | Q(category__icontains=q))
        #data = Product.objects.filter(category__icontains=q)
    else:
        data = Product.objects.all().order_by('-id')


    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))

    paginator = Paginator(data, 8)
    page_num = request.GET.get('page',1)
    data = paginator.page(page_num)
    template_name = 'Customer/search.html'
    context = {'total_item':total_item,'data':data}
    return render(request,template_name,context)


def baseview(request):
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    template_name = 'Customer/base.html'
    context = {'total_item':total_item}
    return render(request,template_name,context)




"""
****class base view****
class Homeview(View):
    def get(self,request):
        Mobile = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')
        topwear = Product.objects.filter(category='TW')
        bottomwear = Product.objects.filter(category='BW')
        Electronic = Product.objects.filter(category='EL')
        homemodels = Product.objects.filter(category='HM')
        template_name = 'Product/home.html'
        context = {'Mobile':Mobile, 'laptop':laptop, 'topwear':topwear,
               'bottomwear':bottomwear,'Electronic':Electronic,
               'homemodels':homemodels}
        return render(request,template_name,context)
"""


def productdetail(request,pk):
    product = Product.objects.get(pk=pk)
    item_in_cart = False
    if request.user.is_authenticated:
        item_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))

    template_name = 'Customer/productdetail.html'
    context = {'product':product,'total_item':total_item,'item_in_cart':item_in_cart}
    return render(request,template_name,context)
"""
***class base view ***
class ProductDetailView(View):
    def get(self, request,pk)
        product = Product.objects.get(pk=pk)
        template_name = 'Customer/productdetail.html'
        context = {'product':product}
    return render(request,template_name,context)
"""

@login_required(login_url='login')
def addtocart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('cart')


@login_required(login_url='login')
def showcart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        total_item = 0
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))

        amount = 0.0
        shiping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for x in cart_product:
                tempamount = (x.quantity * x.product.discout_price)
                amount += tempamount
                total_amount = amount + shiping_amount
                total_item = 0
                if request.user.is_authenticated:
                    total_item = len(Cart.objects.filter(user=request.user))
                template_name = 'Customer/addtocart.html'
                context = {'cart': cart, 'tempamount':tempamount,'amount':amount,'total_amount':total_amount,'total_item':total_item}
            return render(request,template_name,context)
        else:
            template_name = 'Customer/emptycart.html'
            context = {'total_item':total_item}
            return render(request,template_name,context)

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shiping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for x in cart_product:
            tempamount = (x.quantity * x.product.discout_price)
            amount += tempamount
        data = {'quantity': c.quantity,'amount': amount,'total_amount': amount + shiping_amount}
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shiping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for x in cart_product:
                tempamount = (x.quantity * x.product.discout_price)
                amount += tempamount
                #print(total_amount)
        data = {'quantity': c.quantity,
                'amount': amount,
                'total_amount': amount + shiping_amount}
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get( Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shiping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for x in cart_product:
                tempamount = (x.quantity * x.product.discout_price)
                amount += tempamount
                #print(total_amount)
        data = {'amount': amount,
                'total_amount': amount + shiping_amount}
        return JsonResponse(data)

#
# def addproduct(request):
#
#     form = ProductModelForm()
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#     template_name = 'Customer/addproduct.html'
#     total_item = 0
#     if request.user.is_authenticated:
#         total_item = len(Cart.objects.filter(user=request.user))
#     context = {'form': form,'total_item':total_item}
#     return render(request,template_name,context)


def mobileview(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='Mobile')
    elif data == 'Redmi' or data == 'Samsung':
        mobiles = Product.objects.filter(category='Mobile').filter(brand=data)
    elif data == 'Huawei' or data == 'Apple':
        mobiles = Product.objects.filter(category='Mobile').filter(brand=data)
    elif data == 'Xiaomi' or data == 'Oppo':
        mobiles = Product.objects.filter(category='Mobile').filter(brand=data)
    elif data == 'Vivo' or data == 'Nokia':
        mobiles = Product.objects.filter(category='Mobile').filter(brand=data)
    elif data == 'Sony' or data == 'LG':
        mobiles = Product.objects.filter(category='Mobile').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='Mobile').filter(discout_price__lt=15000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='Mobile').filter(discout_price__gt=15000)
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    template_name = 'Customer/filterproduct/mobile.html'
    context = {'mobiles': mobiles,'total_item':total_item}
    return render(request,template_name,context)

def shoesview(request, data=None):
    if data == None:
        Shoesdata = Product.objects.filter(category='Shoes')
    elif data == 'Nike' or data == 'adidas':
        Shoesdata = Product.objects.filter(category='Shoes').filter(brand=data)
    elif data == 'Balance' or data == 'ASICS':
        Shoesdata = Product.objects.filter(category='Shoes').filter(brand=data)
    elif data == 'PUMA' or data == 'Skechers':
        Shoesdata = Product.objects.filter(category='Shoes').filter(brand=data)
    elif data == 'Fila' or data == 'Bata':
        Shoesdata = Product.objects.filter(category='Shoes').filter(brand=data)
    elif data == 'Burberry' or data == 'Corporation':
        Shoesdata = Product.objects.filter(category='Shoes').filter(brand=data)
    elif data == 'below':
        Shoesdata = Product.objects.filter(category='Shoes').filter(discout_price__lt=15000)
    elif data == 'above':
        Shoesdata = Product.objects.filter(category='Shoes').filter(discout_price__gt=15000)
    elif data == 'min':
        Shoesdata = Product.objects.filter(category='Shoes').order_by('discout_price')
    elif data == 'max':
        Shoesdata = Product.objects.filter(category='Shoes').order_by('-discout_price')
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    template_name = 'Customer/filterproduct/Shoes.html'
    context = {'Shoesdata': Shoesdata,'total_item':total_item}
    return render(request,template_name,context)

def topwearview(request, data=None):
    if data == None:
        topwear = Product.objects.filter(category='Top Wear')
    elif data == 'ARMANI' or data == 'FENDI':
        topwear = Product.objects.filter(category='Top Wear').filter(brand=data)
    elif data == 'HOUSE' or data == 'BURBERRY':
        topwear = Product.objects.filter(category='Top Wear').filter(brand=data)
    elif data == 'RALPH' or data == 'LOUIS':
        topwear = Product.objects.filter(category='Top Wear').filter(brand=data)
    elif data == 'CHANEL' or data == 'PRADA':
        topwear = Product.objects.filter(category='Top Wear').filter(brand=data)
    elif data == 'HERMES' or data == 'GUCCI':
        topwear = Product.objects.filter(category='Top Wear').filter(brand=data)
    elif data == 'below':
        topwear = Product.objects.filter(category='Top Wear').filter(discout_price__lt=1500)
    elif data == 'above':
        topwear = Product.objects.filter(category='Top Wear').filter(discout_price__gt=1500)
    elif data == 'min':
        topwear = Product.objects.filter(category='Top Wear').order_by('price')
    elif data == 'max':
        topwear = Product.objects.filter(category='Top Wear').order_by('-price')
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    template_name = 'Customer/filterproduct/topwear.html'
    context = {'topwear': topwear,'total_item':total_item}
    return render(request,template_name,context)

def topwearvieww(request):
    topwearlists = Product.objects.filter(category='Top Wear')
    page = request.GET.get('page', 2)

    paginator = Paginator(topwearlists, 6)
    try:
        topwear = paginator.page(page)
    except PageNotAnInteger:
        topwear = paginator.page(1)
    except EmptyPage:
        topwear = paginator.page(paginator.num_pages)
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))

    return render(request, 'Customer/filterproduct/topwear.html', {'topwear': topwear,'total_item':total_item})





def bottomwear(request, data=None):
    if data == None:
        bottom = Product.objects.filter(category='Bottom Wear')
    elif data == 'Fabindia' or data == 'Chumbak':
        bottom = Product.objects.filter(category='Bottom Wear').filter(brand=data)
    elif data == 'Shatranj' or data == 'Morpankh':
        bottom = Product.objects.filter(category='Bottom Wear').filter(brand=data)
    elif data == 'Rajvila' or data == 'Sttoffa':
        bottom = Product.objects.filter(category='Bottom Wear').filter(brand=data)
    elif data == 'Aglobi' or data == 'Florence':
        bottom = Product.objects.filter(category='Bottom Wear').filter(brand=data)
    elif data == 'Aurelia' or data == 'Indigo':
        bottom = Product.objects.filter(category='Bottom Wear').filter(brand=data)
    elif data == 'below':
        bottom = Product.objects.filter(category='Bottom Wear').filter(discout_price__lt=1000)
    elif data == 'above':
        bottom = Product.objects.filter(category='Bottom Wear').filter(discout_price__gt=1000)
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    template_name = 'Customer/filterproduct/bottomwear.html'
    context = {'bottom': bottom,'total_item':total_item}
    return render(request,template_name,context)





@login_required(login_url='login')
def profileview(request):
    form = CustomerProfileForm()
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            area_name = form.cleaned_data['area_name']
            street_name = form.cleaned_data['street_name']
            house_no = form.cleaned_data['house_no']
            add = Customer(user=user, first_name=first_name, last_name=last_name, gender=gender, country=country, state=state, city=city, area_name=area_name,
                           street_name=street_name, house_no=house_no)
            add.save()
            messages.success(request, 'Congratulations!! your Profile Updated Successfully!!!')
            form = CustomerProfileForm()
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    template_name = 'Customer/profile.html'
    context = {'form':form,'active':'btn-dark','total_item':total_item}
    return render(request, template_name, context)


@login_required(login_url='login')
def addressview(request):
    address = Customer.objects.filter(user=request.user)

    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    template_name = 'Customer/address.html'
    context = {'total_item': total_item,'active': 'btn-dark','address':address}
    return render(request, template_name, context)

"""
def signupview(request):
    form = RegistrationForm()
    form1 = UserForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        form1 = UserForm(request.POST)
        if form.is_valid() and form1.is_valid():
            messages.success(request, 'Congratulation !! Registration can be completed then varify your mail and login!! Thank you ')
            user1 = form1.save()
            pw = user1.password
            user1.set_password(pw)
            user1.save()
            form2 = form.save(commit=False)
            form2.user = user1
            city = City.objects.get(city_name=form.cleaned_data.get('city'))
            addre = Address.objects.create(area_name=form.cleaned_data.get('area_name'),
                                          street_name=form.cleaned_data.get('street_name'),
                                          house_no=form.cleaned_data.get('street_name'),
                                          area_pincode=form.cleaned_data.get('street_name'),
                                          city = city)
            form.address =  addre

            form.save()
            return redirect('signup')

    template_name = 'Customer/register.html'
    context = {'form': form,'form1':form1}
    return render(request,template_name,context)
"""
# def signinview(request):
#     if request.method == 'POST':
#         u = request.POST.get('un')
#         p = request.POST.get('pw')
#         #log = User.objects.get(username=u)
#         user = authenticate(username=u, password=p)
#         user1 = User.objects.get(username=u)
#         customer = Customer.objects.get(user=user1)
#
#         print(user1)
#         if user is not None:
#             if customer.is_seller:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 login(request, user)
#                 return redirect('mobile')
#         else:
#             messages.error(request,"Invalid Username or Password")
#     template_name = 'Customer/login.html'
#     context = {}
#     return render(request,template_name,context)



def customerregiview(request):
    form = CustomerRegistrationForm()
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation !! Registration can be completed then varify your mail and login!! Thank you ')
            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your eCommerce Applications Account'
            message = render_to_string('Customer/registrationmail/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('registration')
    template_name = 'Customer/register.html'
    context = {'form': form}
    return render(request, template_name, context)


def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def signoutview(request):
    logout(request)
    #messages.info(request, "You have successfully logged out.")
    return redirect('login')

import razorpay
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='login')
def checkoutview(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_item = Cart.objects.filter(user=user)
    amount= 0.0
    shiping_amount = 70.0
    total_amount= 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for x in cart_product:
            tempamount = (x.quantity * x.product.discout_price)
            amount += tempamount
        total_amount = shiping_amount + amount
        total_amount1 = int(shiping_amount + amount ) * 100
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))

    template_name = 'Customer/checkout.html'
    context = {'add':add,'cart_item':cart_item,'total_amount':total_amount,'total_item':total_item}
    return render(request,template_name,context)





@login_required(login_url='login')
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaces(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@login_required(login_url='login')
def ordersview(request):
    order = OrderPlaces.objects.filter(user=request.user)
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    template_name = 'Customer/orders.html'
    context = {'order':order,'total_item':total_item}
    return render(request, template_name, context)



def index(request):
    if request.method == 'POST':
        name= request.user
        #name = request.POST.get('name')
        #amount = request.POST.get('amount')
        print(name)
        start_amount = 0.0
        shiping_amount = 70.0
        amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for x in cart_product:
                tempamount = (x.quantity * x.product.discout_price)
                start_amount += tempamount
                amount = int(shiping_amount + start_amount) * 100
        print(amount)
        client = razorpay.Client(auth=("rzp_test_AeJ4sJjY6CejF5", "TQAai5IuODZsctn8dMOcCYeT"))
        payments = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture' : 1})
        payment = Payment(name=name,amount=amount, payment_id= payments['id'])
        payment.save()
        return render(request, 'Customer/index.html',{'payment':payment})
    return render(request, 'Customer/index.html', {})

@csrf_exempt
def successview(request):
    if request.method == 'POST':
        a = request.POST
        print(a)
        order_id = ""
        for key , val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        print(order_id)
        user = Payment.objects.filter(payment_id=order_id).first()
        #user.paid = True
        #user.save()
    template_name = 'Customer/success.html'
    context = {'user':user}
    return render(request, template_name, context)



from django.views.decorators.csrf import csrf_exempt


# def paymentview(request):
#     if request.method == "POST":
#         name = request.POST.get('name')
#         amount = 50000 *100
#
#         client = razorpay.Client(auth=("TEST_KEY", "SECRET_KEY"))
#
#         payment = client.order.create({'amount': amount, 'currency': 'INR','payment_capture': '1'})
#         return render(request, 'Customer/paymentgatway/payment.html',{'payment':payment})
#     return render(request, 'Customer/paymentgatway/payment.html')
#
# @csrf_exempt
# def success(request):
#     return render(request, "Customer/paymentgatway/success.html")

from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt




#working code

# def home(request):
#     if request.method == "POST":
#         name = request.user
#         amount = 50000
#         print(name)
#         client = razorpay.Client(auth=("rzp_test_AeJ4sJjY6CejF5", "TQAai5IuODZsctn8dMOcCYeT"))
#         payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
#         return render(request, 'Customer/index.html',{'payment':payment})
#     return render(request, 'Customer/index.html')
#
# @csrf_exempt
# def success(request):
#     return render(request, "Customer/success.html")



