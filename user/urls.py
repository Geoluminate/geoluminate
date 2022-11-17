from django.urls import path, include
from user.views import user_settings, profile, dashboard

app_name = 'user'
urlpatterns = [
    path("accounts/", include('allauth.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    path('settings/', user_settings, name='settings'),
    path('profile/', profile, name='profile'),
]
