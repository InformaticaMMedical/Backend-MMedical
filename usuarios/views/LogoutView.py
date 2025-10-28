from rest_framework.response import Response
from rest_framework.views import APIView

class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logout exitoso"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
