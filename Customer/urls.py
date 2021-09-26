from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm,Mypasswordchange,MypasswordResetForm,MySetPasswordForm


urlpatterns = [
    path('', views.homeview, name='home'),
    #path('register/', views.signupview, name='signup'),
    #path('login/', views.signinview, name='signin'),
    path('registration/', views.customerregiview, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='Customer/login.html',
                                                authentication_form=LoginForm), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.signoutview, name='logout'),
    # path('',views.Homeview.as_view(), name='home'),
    path('productdetail/<int:pk>', views.productdetail, name='productdetail'),
    # path('productdetail/<int:pk>', views.Productdetail.as_view(), name='productdetail'),
    path('add-to-cart/', views.addtocart, name='add-to-cart'),
    path('cart/', views.showcart, name='cart'),
    path('emptycart/', views.showcart, name='emptycart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    #path('addproduct/', views.addproduct, name='addproduct'),
    path('base/', views.baseview, name='base'),
    path('profile/', views.profileview, name='profile'),
    path('address/', views.addressview, name='address'),

    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),


    #filter
    path('topwear/', views.topwearvieww, name='topwear'),
    path('mobile/', views.mobileview, name='mobile'),
    path('mobile/<str:data>', views.mobileview, name='mobiledata'),
    path('topwear/', views.topwearview, name='topwear'),
    path('topwear/<str:data>', views.topwearview, name='topweardata'),
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<str:data>', views.bottomwear, name='bottomwearjeans'),
    path('shoesview/', views.shoesview, name='shoes'),
    path('shoesview/<str:data>', views.shoesview, name='shoesdata'),
    path('checkout/', views.checkoutview, name='checkout'),
    path('search/', views.search, name='search'),
    path('paymentdone/', views.payment_done, name='paymentdone'),


    #payment gatway working
    #path('home/', views.home, name='home'),
    #path('success/', views.success, name='success'),
    path('orders/', views.ordersview, name='orders'),

    # path('paymentgateway', views.paymentview, name='paymentgateway'),

    #payment gateway actually
    path('payment/', views.index, name='payment'),
    path('success/', views.successview, name='success'),





    #reset password
    path('changepassworld/', auth_views.PasswordChangeView.as_view(template_name='Customer/changepassword/changepassword.html',
                form_class=Mypasswordchange, success_url='/passwordchangedone/'), name='changepass'),

    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='Customer/changepassword/changepassworddone.html'),
         name='passwordchangedone'),


    #forgotpassword
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='Customer/forgotpassword/password_reset.html',form_class=MypasswordResetForm),
                                                                name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Customer/forgotpassword/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='Customer/forgotpassword/password_reset_confirm.html', form_class=MySetPasswordForm),
                                                                                                name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='Customer/forgotpassword/password_reset_complete.html'),
                                                                            name='password_reset_complete'),


]