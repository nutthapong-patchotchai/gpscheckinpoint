from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from checkin.models.user import profile


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(required=False, write_only=True, allow_blank=True)
    password1 = serializers.CharField(required=False, write_only=True, allow_blank=True)
    password2 = serializers.CharField(required=False, write_only=True, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    geo = serializers.IntegerField(required=False)
    amphur = serializers.IntegerField(required=False)
    province = serializers.IntegerField(required=False)
    district = serializers.IntegerField(required=False)
    post = serializers.CharField(required=False, allow_blank=True)
    tel = serializers.CharField(required=False, allow_blank=True)
    faculty = serializers.CharField(required=False, allow_blank=True)
    question1 = serializers.IntegerField(required=False)
    question2 = serializers.IntegerField(required=False)
    question3 = serializers.IntegerField(required=False)
    address2 = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        password = attrs.get("password") or attrs.get("password1")
        password2 = attrs.get("password2") or password
        username = (attrs.get("username") or attrs.get("email") or "").strip()

        if not username:
            raise serializers.ValidationError({"username": "กรุณาระบุชื่อผู้ใช้หรืออีเมล"})
        if not password:
            raise serializers.ValidationError({"password": "กรุณาระบุรหัสผ่าน"})
        if password != password2:
            raise serializers.ValidationError({"password2": "รหัสผ่านไม่ตรงกัน"})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "ชื่อผู้ใช้นี้ถูกใช้งานแล้ว"})

        attrs["username"] = username
        attrs["password"] = password
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

        profile_fk_fields = ("geo", "amphur", "province", "district")
        if all(validated_data.get(field) for field in profile_fk_fields):
            profile.objects.create(
                user=user,
                address=validated_data.get("address", ""),
                geo_id=validated_data.get("geo"),
                amphur_id=validated_data.get("amphur"),
                province_id=validated_data.get("province"),
                district_id=validated_data.get("district"),
                post=validated_data.get("post", ""),
                tel=validated_data.get("tel", ""),
                faculty=validated_data.get("faculty", ""),
                question1=validated_data.get("question1", 0),
                question2=validated_data.get("question2", 0),
                question3=validated_data.get("question3", 0),
                address2=validated_data.get("address2", ""),
            )
        return user


def user_payload(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_staff": user.is_staff,
    }


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return redirect("/register/")

    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response(
            {"token": token.key, "key": token.key, "user": user_payload(user)},
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        username = request.data.get("username") or request.data.get("email")
        password = request.data.get("password")
        if username and "@" in username:
            username = User.objects.filter(email=username).values_list("username", flat=True).first()

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {"detail": "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        login(request, user)
        token, _created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "key": token.key, "user": user_payload(user)})


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if request.auth:
            request.auth.delete()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
