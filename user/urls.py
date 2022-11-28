from django.urls import path, include
from user import views

app_name = 'user'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.Account.as_view(), name='account'),
    path('profile/', views.profile, name='profile'),
]
