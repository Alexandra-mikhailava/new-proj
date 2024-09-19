"""
URL configuration for my_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from main import views as main_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', main_views.home, name="home"),
    path('services/', main_views.services_list, name='services_list'),  # Путь для списка услуг
    path('service/<int:service_id>/', main_views.service_detail, name='service_detail'),  # Путь для услуги по ID
    path('contacts/', main_views.contacts, name="contacts"),
    #path('test/<path:test_param>/', main_views.test_url),
    #path('test/<str:test_param>/', main_views.test_url),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('test/', main_views.test)
]

urlpatterns += [ path('accounts/', include('django.contrib.auth.urls')),]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
