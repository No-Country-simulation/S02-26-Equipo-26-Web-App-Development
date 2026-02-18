"""
URL configuration for at_manager project.

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

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth
    path('api/auth/', include('apps.users.urls')),
    
    # APIs de las otras apps
    path('api/caregivers/', include('apps.caregivers.urls')),
    path('api/documents/', include('apps.documents.urls')),
    path('api/patients/', include('apps.patients.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/shifts/', include('apps.shifts.urls')),
]