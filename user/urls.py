from django.urls import path
from user.views import user_settings, Dashboard, profile

app_name = 'user'
urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('settings/', user_settings, name='settings'),
    path('profile/', profile, name='profile'),

]
