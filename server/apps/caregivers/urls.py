# server/apps/caregivers/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CaregiverViewSet, SpecialtyViewSet

router = DefaultRouter()
router.register(r'', CaregiverViewSet, basename='caregiver')

urlpatterns = [
    path('', include(router.urls)),
    # Endpoint separado para especialidades (opcional, también está como action)
    path('specialties/', SpecialtyViewSet.as_view({'get': 'list'}), name='specialties-list'),
]