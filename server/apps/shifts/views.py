from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import ShiftReport
from .serializers import ShiftReportSerializer


class ShiftReportViewSet(viewsets.ModelViewSet):
    queryset = ShiftReport.objects.all()
    serializer_class = ShiftReportSerializer
    permission_classes = [AllowAny]