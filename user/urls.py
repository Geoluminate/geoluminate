from django.urls import path
from user.views import user_settings, Dashboard

app_name = 'user'
urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('settings/', user_settings, name='settings'),

]
