from rest_framework import serializers
from .models import SignUp , StudentDetails

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignUp
        fields = ["userName","email","password"]

class LoginSerializer(serializers.Serializer):
    userName = serializers.CharField()
    password = serializers.CharField()

class StudentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetails
        fields = '__all__' 