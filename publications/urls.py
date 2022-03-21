from publications import views
from django.urls import path

app_name = 'publications'
urlpatterns = [
    path('',views.PublicationListView.as_view(), name='list'),
    path('claim-confirmed/',views.claim_confirmed, name='claim_confirmed'),
    path('<pk>/',views.PublicationDetailsView.as_view(), name='detail'),
    path('verify/<pk>/',views.verify, name='verify'),
    path('claim/<pk>/',views.claim, name='claim'),
]
