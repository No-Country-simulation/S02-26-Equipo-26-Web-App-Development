from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LocationViewSet, UserViewSet, AdminViewSet,
    CaregiverViewSet, PatientViewSet, FamilyViewSet
)

router = DefaultRouter()
router.register(r'locations', LocationViewSet)
router.register(r'all', UserViewSet, basename='user')
router.register(r'admins', AdminViewSet)
router.register(r'caregivers', CaregiverViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'families', FamilyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]