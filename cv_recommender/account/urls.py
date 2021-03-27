from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('applicantdashboard/', views.applicantdashboard,
         name='applicantdashboard'),
    path('recruiterdashboard/', views.recruiterdashboard,
         name='recruiterdashboard'),

]
