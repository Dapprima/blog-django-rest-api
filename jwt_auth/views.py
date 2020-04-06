from rest_framework import permissions
from rest_framework import views
from .serializers import UserCreateSerializer
from rest_framework.generics import CreateAPIView


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

