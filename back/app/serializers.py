#from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
        #idを更新不可にできる
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'required': True}}


    def create(self,validated_data):
        #パスワードをハッシュ化する
        user = User.objects.create_user(**validated_data)
        return user

