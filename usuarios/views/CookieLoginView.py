from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name="dispatch")
class CookieLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        print(f"Username: {username}")
        password = request.data.get("password")
        print(f"Password: {password}")
        remember = request.data.get("remember", False)
        print(f"Remember: {remember}")

        user = authenticate(request, username=username, password=password)
        print(f"Resultado authenticate(): {user}")

        if not user:
            return Response({"detail": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        access_age = 60 * 15
        refresh_age = 60 * 60 * 24 * (30 if remember else 7)

        response = Response({
            "message": "Login exitoso",
            "user": {"id": user.id, "username": user.username, "email": user.email},
        })

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="None",
            max_age=access_age,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="None",
            max_age=refresh_age,
        )

        return response
