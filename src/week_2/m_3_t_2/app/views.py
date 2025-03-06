from app.serializers import UserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            response = super().post(request, *args, **kwargs)
            response.data["message"] = "User created successfully"
            return response
        return Response(user_serializer.errors, status.HTTP_400_BAD_REQUEST)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Protected route is working"}, status.HTTP_200_OK)
