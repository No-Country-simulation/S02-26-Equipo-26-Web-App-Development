from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.users.models import ShiftReport
from .serializers import ShiftReportSerializer


class ShiftReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Shift Reports
    """
    queryset = ShiftReport.objects.all()
    serializer_class = ShiftReportSerializer
    permission_classes = [IsAuthenticated]
