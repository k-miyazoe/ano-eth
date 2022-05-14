from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    #管理者のみユーザーリスト確認可能
    permission_classes = (permissions.IsAdminUser,)


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )