from publications import views
from django.urls import path

app_name = 'publications'
urlpatterns = [
    path('',views.PublicationList.as_view(), name='list'),
    path('<pk>/',views.PublicationDetail.as_view(), name='detail'),
    path('author/<pk>/',views.AuthorDetail.as_view(), name='author_detail'),

]
