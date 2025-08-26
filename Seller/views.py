from django.contrib.messages import MessageFailure
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from Customer.models import Product, Cart


from django.contrib.sites.shortcuts import get_current_site


# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max, Min
from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes, force_str
from django.utils.encoding import force_bytes, force_str

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
    laptop = Product.objects.filter(category='L')
    Shoesdata = Product.objects.filter(category='Shoes')
    topwear = Product.objects.filter(category='Top Wear')
    bottomwear = Product.objects.filter(category='Bottom Wear')
    Electronic = Product.objects.filter(category='EL')
    homemodels = Product.objects.filter(category='HM')
    template_name = 'Seller/home.html'
    context = {'Mobile':Mobile, 'Shoesdata':Shoesdata,'laptop':laptop, 'topwear':topwear,
               'bottomwear':bottomwear,'Electronic':Electronic,
               'homemodels':homemodels}
    return render(request,template_name,context)

def baseview(request):
    template_name = 'Seller/base.html'
    context = {}
    return render(request,template_name,context)

@login_required(login_url='login1')
def deleteproductview(request,id):
    demo = Product.objects.get(id=id)
    if request.method == 'POST':
        demo.delete()
        return redirect('home1')

    template_name = 'Seller/deleteproductview.html'
    context = {'demo':demo}
    return render(request,template_name,context)

@login_required(login_url='login1')
def updateproductview(request,id):
    obj = Product.objects.get(id=id)
    form = ProductModelForm(instance=obj)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('home1')
    template_name = 'Seller/update.html'
    context = {'form':form}
    return render(request,template_name,context)


@login_required(login_url='login1')
def profileview(request):
    form = SellerProfileForm()
    if request.method == 'POST':
        form = SellerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            mobile_no = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            product_category = form.cleaned_data['product_category']
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            gst_no = form.cleaned_data['gst_no']
            add = Seller(user=user, first_name=first_name, last_name=last_name, mobile_no=mobile_no, gender=gender, product_category=product_category, country=country, state=state,
                         city=city, bank_name=bank_name, account_no=account_no, gst_no=gst_no)
            add.save()
            messages.success(request, 'Congratulations!! your Profile Updated Successfully!!!')
            form = SellerProfileForm()
    template_name = 'Seller/profile.html'
    context = {'form':form,'active':'btn-primary'}
    return render(request, template_name, context)


def addproduct(request):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home1')
    template_name = 'Seller/addproduct.html'
    context = {'form': form}
    return render(request,template_name,context)


@login_required(login_url='login1')
def addressview(request):
    address = Seller.objects.filter(user=request.user)
    template_name = 'Seller/address.html'
    context = {'active': 'btn-primary','address':address}
    return render(request, template_name, context)


def sellerregiview(request):
    form = SellerRegistrationForm()
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation !! Registration can be completed then varify your mail and login!! Thank you ')
            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your eCommerce Applications Account'
            message = render_to_string('Seller/registrationmail/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('registration1')
    template_name = 'Seller/register.html'
    context = {'form': form}
    return render(request, template_name, context)

def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def loginview(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form)
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('profile1')
        else:
            messages.error(request,' Login Must be \n 1] Verify your Email Address,2] Please Insert currect Username and Password')
            return redirect('login1')
    template_name = 'Seller/login.html'
    context = {'form':form}
    return render(request,template_name,context)


def signoutview(request):
    logout(request)
    #messages.info(request, "You have successfully logged out.")
    return redirect('login1')


def sellerproductview(request):
    user=request.user
    product = Product.objects.filter(category=request.user)
    seller = Seller.objects.get(user=user)
    address = Seller.objects.filter(user=request.user)
    address1 = Seller.objects.filter(product_category=request.user)
    print(address)
    print(user)
    print(product)
    print(seller)
    print(address1)
    template_name = 'Seller/sellerproduct.html'
    context = {'product':product,'address':address}
    return render(request,template_name,context)