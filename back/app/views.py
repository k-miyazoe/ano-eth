from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer

#from rest_framework import viewsets
#from django.contrib.auth import get_user_model
#from django.shortcuts import render,redirect
#from django.utils.decorators import method_decorator

class UserList(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    #permission_classes = (permissions.IsAdminUser, )