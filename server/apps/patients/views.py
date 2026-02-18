from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.users.models import Patient
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Patients.
    
    IMPORTANTE: Patient usa user_id como primary key.
    Las URLs usan el user_id, no un id separado.
    
    Endpoints disponibles:
    - GET /api/patients/ → Listar todos los pacientes
    - GET /api/patients/user_id/ → Ver detalle de un paciente
    - PATCH /api/patients/user_id/ → Actualizar medical_history
    - DELETE /api/patients/user_id/ → Eliminar paciente (opcional)
    
    NO permite POST — los pacientes se crean vía /api/auth/register/
    """
    queryset = Patient.objects.select_related('user').all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    # CRÍTICO: Como Patient usa user como PK, el lookup field es 'user'
    lookup_field = 'user'
    
    # Deshabilitar el método POST (create)
    def create(self, request, *args, **kwargs):
        return Response(
            {
                'error': 'No podés crear pacientes directamente desde este endpoint.',
                'message': 'Usá POST /api/auth/register/ con role="Patient"',
                'hint': 'Ejemplo: {"email": "...", "password": "...", "role": "Patient", "medical_history": "..."}'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    # Opcional: obtener el paciente del usuario autenticado
    @action(detail=False, methods=['get'], url_path='me')
    def my_patient_profile(self, request):
        """
        GET /api/patients/me/
        Devuelve el perfil de paciente del usuario autenticado.
        Solo funciona si el usuario es Patient.
        """
        if request.user.role != 'Patient':
            return Response(
                {'error': 'No tenés un perfil de paciente'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            patient = Patient.objects.get(user=request.user)
            serializer = self.get_serializer(patient)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Perfil de paciente no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )