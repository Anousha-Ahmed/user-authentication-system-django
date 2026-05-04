from django.urls import path
from . import views
from .views import (
    SignUpView, LoginView, StudentDetailsView, VerifyOTPView, ResendOTPView,
    ForgotPasswordView, ResetPasswordView, UpdatePasswordView, LogoutView
)

urlpatterns = [
    # APIs 
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('update-password/', UpdatePasswordView.as_view(), name='update_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('check-session/', views.CheckSessionView.as_view(), name='check_session'),
    
    # Student APIs 
    path('students/', StudentDetailsView.as_view(), name='students'),
    path('students/<int:pk>/', StudentDetailsView.as_view(), name='student_detail'),
    
    # HTML Pages
    path('signup-page/', views.signup_page, name='signup_page'),
    path('login-page/', views.login_page, name='login_page'),
    path('verify-otp-page/', views.verify_otp_page, name='verify_otp_page'),
    path('forgot-password-page/', views.forgot_password_page, name='forgot_password_page'),
    path('reset-password-page/', views.reset_password_page, name='reset_password_page'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('students-page/', views.students_page, name='students_page'), 
]