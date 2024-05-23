from django.urls import path, reverse_lazy
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    # Registration and Verification
    path('register/', register_user, name='register'),
    path('register/email_verification_sent/',
         lambda request: render(
             request, 'email_verification_sent.html'),
         name='email_verification_sent'
         ),
    # Login and Logout
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    # Dashboard
    path('dashboard/', dashboard_user, name='dashboard'),
    path('profile_management/', profile_user, name='profile_management'),
    path('delete_user/', delete_user, name='delete_user'),

    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password/password_reset.html',
        email_template_name='password/password_reset_email.html',
        success_url=reverse_lazy('account:password_reset_done')
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password/password_reset_done.html'
    ), name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password/password_reset_confirm.html',
        success_url=reverse_lazy('account:password_reset_complete'),
        form_class=CustomSetPasswordForm
    ), name='password_reset_confirm'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password/password_reset_complete.html'),
        name='password_reset_complete'),
]
