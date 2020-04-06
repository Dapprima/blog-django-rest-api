from django.contrib.auth.models import User
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
                                     "input_type":   "password"})
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}


    def validate(self, data):
         user = User(**data)
         password = data.get('password')
         errors = dict() 
         try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=User)
        
         # the exception raised here is different than serializers.ValidationError
         except exceptions.ValidationError as e:
             errors['password'] = list(e.messages)

         if errors:
             raise serializers.ValidationError(errors)

         return super(UserCreateSerializer, self).validate(data)