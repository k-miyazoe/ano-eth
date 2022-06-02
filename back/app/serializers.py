#from django.contrib.auth import get_user_model
from dataclasses import field
from rest_framework import serializers
from .models import User,Ether

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password',)
        #idを更新不可にできる
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'required': True}}

    def create(self,validated_data):
        #パスワードをハッシュ化する
        user = User.objects.create_user(**validated_data)
        return user

class EtherSerializer(serializers.ModelSerializer):
    class Meat:
        model = Ether
        field = ('id','user_id','ether_address','ether_password','ether_wallet','ether_anonymous','ether_account_name')
        read_only_fields = ('id',)
    #def create_ether_address(self):
        