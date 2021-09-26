from django.contrib.auth import password_validation
from importlib._common import _

from django import forms
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, \
    PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User

from .models import Seller
from Customer.models import Product


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {'gender': forms.RadioSelect}

class SellerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class': 'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class': 'form-control'}))
    password = forms.CharField(label =_("Password"), strip=False, widget=forms.PasswordInput(attrs={
        'autocomplete':'current-password', 'class':'form-control'}))


class Mypasswordchange(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'Current-password',
                     'autofocu':True, 'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'New-password',
                   'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'New-password',
                     'class':'form-control'}))


class MypasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=250, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'New-password',
                   'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'New-password',
                     'class':'form-control'}))



class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['first_name','last_name','mobile_no','gender','product_category','country','state','city','bank_name','account_no','gst_no']
        widgets = {'first_name':forms.TextInput(attrs={'class':'form-control'}),
                   'last_name':forms.TextInput(attrs={'class':'form-control'}),
                   'mobile_no':forms.TextInput(attrs={'class':'form-control'}),
                   'gender':forms.RadioSelect(attrs={'class':'radio-inline-radio'}),
                   'product_category':forms.Select(attrs={'class':'form-control'}),
                    'country':forms.Select(attrs={'class':'form-control'}), 'state':forms.Select(attrs={'class':'form-control'}),
                   'city':forms.Select(attrs={'class':'form-control'}),'bank_name':forms.TextInput(attrs={'class':'form-control'}),
                   'account_no':forms.TextInput(attrs={'class':'form-control'}),
                   'gst_no':forms.NumberInput(attrs={'class':'form-control'})}