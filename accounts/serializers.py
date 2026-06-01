from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model = User
        fields = ['id','username','email','password','first_name','last_name']
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name','is_staff']

class SocialLoginSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=['google','facebook','github','demo'])
    access_token = serializers.CharField()
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
