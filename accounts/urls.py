from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # password change
    path('password_change/', auth_views.PasswordChangeView.as_view(), 
        name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), 
        name='password_change_done'),

    #password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), 
        name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), 
        name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(), 
        name='password_reset_confirm'),
    path('password_reset/complete/', 
        auth_views.PasswordResetCompleteView.as_view(), 
        name='password_reset_complete'),
]
