from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShiftReportViewSet

router = DefaultRouter()
router.register(r'', ShiftReportViewSet, basename='shiftreport')

urlpatterns = [
    path('', include(router.urls)),
]