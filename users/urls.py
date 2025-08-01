from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView, user_logout, 
    user_profile, update_profile
)

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('auth/logout/', user_logout, name='logout'),
    path('auth/profile/', user_profile, name='profile'),
    path('auth/profile/update/', update_profile, name='update_profile'),
] 