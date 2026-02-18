from __future__ import annotations

from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthenticationMiddleware:
    """
    Middleware opcional para autenticar JWT en vistas Django (no-DRF).

    - Si el request ya tiene un usuario autenticado, no hace nada.
    - Si hay un Authorization Bearer válido, asigna request.user.
    - Ante cualquier error, falla en silencio para no romper el request.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self._jwt_auth = JWTAuthentication()

    def __call__(self, request):
        user = getattr(request, "user", None)
        if not getattr(user, "is_authenticated", False):
            try:
                header = self._jwt_auth.get_header(request)
                if header is not None:
                    raw_token = self._jwt_auth.get_raw_token(header)
                    if raw_token is not None:
                        validated = self._jwt_auth.get_validated_token(raw_token)
                        request.user = self._jwt_auth.get_user(validated)
            except Exception:
                pass

        return self.get_response(request)

