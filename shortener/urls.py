from django.urls import path
from . import views

app_name = 'shortener'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_url, name='create_url'),
    path('edit/<int:pk>/', views.edit_url, name='edit_url'),
    path('delete/<int:pk>/', views.delete_url, name='delete_url'),
    path('detail/<int:pk>/', views.url_detail, name='url_detail'),
]