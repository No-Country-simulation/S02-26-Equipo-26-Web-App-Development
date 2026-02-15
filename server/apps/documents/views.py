from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [AllowAny]  # Cambiar a IsAuthenticated después