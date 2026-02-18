from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CaregiverViewSet

router = DefaultRouter()
router.register(r'', CaregiverViewSet, basename='caregiver')

urlpatterns = [
    path('', include(router.urls)),
]