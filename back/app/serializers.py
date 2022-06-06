from dataclasses import field
from rest_framework import serializers
from .models import User,Ether,Question,Answer

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
    class Meta:
        model = Ether
        fields = '__all__' 
        read_only_fields = ('id',)
    
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('id',)

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ('id',)