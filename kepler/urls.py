from django.urls import path, include
from kepler import views

app_name = 'kepler'
urlpatterns = [
    path('viewer.app',views.KeplerFullPageView.as_view(), name='application'),
]
