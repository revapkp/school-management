from rest_framework import serializers
from django.contrib.auth.models import User

from. models import *


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ['email','password']
