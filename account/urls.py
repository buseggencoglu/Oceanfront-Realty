from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_request, name='login'),
    path('register/', views.role_choose, name='register'),
    path('register_customer/', views.register_customer, name='register_customer'),
    path('register_estate_person/', views.register_estate_person, name='register_estate_person'),
    path('sent/', views.activation_sent_view, name="sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name="activate"),
    path('logout/', views.logout_request, name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='change_password_form.html',
        success_url='/'),
         name='password_change'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password-reset/password_reset.html',
        subject_template_name='password-reset/password_reset_subject.txt',
        email_template_name='password-reset/password_reset_email.html',
        success_url='/login/'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]
