"""
URL configuration for gas_utility_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from customer import views as customer_views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication
    path('register/', customer_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='customer/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='customer/logout.html'), name='logout'),
    
    # Customer
    path('profile/', customer_views.profile, name='customer_profile'),
    path('dashboard/', customer_views.dashboard, name='customer_dashboard'),
    
    # Service Requests
    path('service-requests/', include('service_requests.urls')),
    
    # Support Portal
    path('support/', include('support_portal.urls')),
    
    # Homepage - using a simple template view
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Help page
    path('help/', TemplateView.as_view(template_name='help.html'), name='help'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
