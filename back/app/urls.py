from django.urls import path
from . import views
from .views import *

name="app"

urlpatterns = [
    #User
    path('users/', UserList.as_view()),
    path('create-user/',UserCreate.as_view()),
    path('users/<pk>/', UserRetrieveUpdate.as_view()),
    #web3
    path('create-eth-address/', views.createEtherAddress),
    #Ether
    path('ether-list/', EtherList.as_view()),
    path('create-ether/', EtherCreate.as_view()),
    #Question
    path('question-list/', QuestionList.as_view()),
    path('create-question/', QuestionCreate.as_view()),
    #Answer
    path('create-answer/', AnswerCreate.as_view()),
]
