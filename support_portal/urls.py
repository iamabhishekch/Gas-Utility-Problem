from django.urls import path
from . import views

urlpatterns = [
    path('', views.support_dashboard, name='support_dashboard'),
    path('request/<int:pk>/', views.request_detail, name='support_request_detail'),
]
