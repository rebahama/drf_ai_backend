from dj_rest_auth.serializers import LoginSerializer, JWTSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class CustomLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        print("CustomLoginSerializer called")
        user = self.user
        refresh = RefreshToken.for_user(user)

        data["access"] = str(refresh.access_token)
        data["refresh"] = str(refresh)
        data["user"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }

        return data


class CustomJWTSerializer(JWTSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        print("CustomLoginSerializer called")
        user = self.user
        data["user"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return data