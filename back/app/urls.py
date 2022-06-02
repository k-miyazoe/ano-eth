from django.urls import path
from . import views
from .views import *

name="app"

urlpatterns = [
    #User
    path('users/', UserList.as_view()),
    path('create-user/',UserCreate.as_view()),
    path('users/<pk>/', UserRetrieveUpdate.as_view()),
    #Ether
    path('create-eth-address/', views.createEtherAddress),
]
