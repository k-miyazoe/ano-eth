from django.urls import path
from . import views
from .views import *

name="app"

urlpatterns = [
    #User
    path('users/', UserList.as_view()),
    path('create-user/',UserCreate.as_view()),
    path('users/<pk>/', UserRetrieveUpdate.as_view()),
    
    #WEB3
    path('create-eth-address/', views.createEtherAddress),
    #Ether
    path('ether-get/<int:user_id>', EtherGet.as_view()),
    path('create-ether/', EtherCreate.as_view()),
    path('ether/<pk>/', EtherRetrieveUpdate.as_view()),
    
    #Question
    path('get-question/<slug:flag>/', QuestionList.as_view()),
    path('get-question/<pk>', QuestionGet.as_view()),
    path('create-question/', QuestionCreate.as_view()),
    # path('update-question/<pk>/', QuestionUpdate.as_view()),
    # path('search-question/<slug:flag>', QuestionSearch.as_view()),
    
    #Answer
    path('get-answer/<int:question_id>/', AnswerGet.as_view()),
    path('create-answer/', AnswerCreate.as_view()),
    path('update-answer/<pk>/', AnswerUpdate.as_view()),
]