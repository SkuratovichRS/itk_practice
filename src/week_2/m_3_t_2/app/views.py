from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from app.serializers import UserSerializer


class RegisterView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status.HTTP_400_BAD_REQUEST)
        user_serializer.save()
        response = super().post(request, *args, **kwargs)
        response.data["message"] = "User created successfully"
        return response
        


class LogoutView(TokenRefreshView):
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        token = RefreshToken(request.data["refresh"])
        token.blacklist()
        return Response(
            {"message": "User logged out successfully"}, status.HTTP_201_CREATED
        )


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Protected route is working"}, status.HTTP_200_OK)
