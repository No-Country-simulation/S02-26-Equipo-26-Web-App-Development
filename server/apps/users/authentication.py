from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class EmailLoginView(APIView):
    """
    Login personalizado que usa email en lugar de username
    """
    permission_classes = []  # Permitir acceso sin autenticación
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Email y password son requeridos'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
            
            # Verificar password (comparación directa por ahora)
            if user.password != password:
                return Response(
                    {'error': 'Credenciales inválidas'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Generar tokens JWT manualmente
            refresh = RefreshToken()
            refresh['user_id'] = user.user_id
            refresh['email'] = user.email
            refresh['role'] = user.role
            refresh['first_name'] = user.first_name
            refresh['last_name'] = user.last_name
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'user_id': user.user_id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                }
            })
            
        except User.DoesNotExist:
            return Response(
                {'error': 'Credenciales inválidas'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )