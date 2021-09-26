from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from .forms import LoginForm,Mypasswordchange,MypasswordResetForm,MySetPasswordForm

urlpatterns = [
    path('homeseller/', homeview, name='home1'),
    path('base/', baseview, name='base'),
    path('addproduct/', addproduct, name='addproduct1'),
    path('updatebasics/<int:id>/', updateproductview, name='updateproduct'),
    path('deletebasics/<int:id>/', deleteproductview, name='dltbasics'),
    path('registration/', sellerregiview, name='registration1'),

    #path('login/', auth_views.LoginView.as_view(template_name='Seller/login.html',
                                                #authentication_form=LoginForm), name='login1'),
    path('login', loginview, name='login1'),

    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', signoutview, name='logout1'),
    path('profile/', profileview, name='profile1'),
    path('address/', addressview, name='address1'),
    path('sellerproduct/', sellerproductview, name='sellerproduct'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),


    #reset password
    path('changepassworld/', auth_views.PasswordChangeView.as_view(template_name='Seller/changepassword/changepassword.html',
                                                                    form_class=Mypasswordchange, success_url='Seller/passwordchangedonee/'), name='changepass1'),

    path('passwordchangedonee/', auth_views.PasswordChangeDoneView.as_view(template_name='Seller/changepassword/changepassworddone.html'),
                                                                            name='passwordchangedonee'),

    # forgotpassword
    path('password-reset1/', auth_views.PasswordResetView.as_view(template_name='Seller/forgotpassword/password_reset.html',
                                                                     form_class=MypasswordResetForm), name='password_reset1'),
    path('password-reset1/done/', auth_views.PasswordResetDoneView.as_view(template_name='Seller/forgotpassword/password_reset_done.html'),
                                                                        name='password_reset_done1'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='Seller/forgotpassword/password_reset_confirm.html', form_class=MySetPasswordForm),
         name='password_reset_confirm1'),
    path('password-reset-complete1/', auth_views.PasswordResetCompleteView.as_view(
        template_name='Seller/forgotpassword/password_reset_complete.html'),
         name='password_reset_complete1'),
]