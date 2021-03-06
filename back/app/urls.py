from django.urls import path
from . import views
from .views import *

name="app"

urlpatterns = [
    #User
    path('users/', UserList.as_view()),
    path('create-user/',UserCreate.as_view()),
    path('users/<pk>/', UserRetrieveUpdate.as_view()),
    path('user-delete/<pk>/', UserDelete.as_view()),
    
    #WEB3
    path('create-eth-address/', views.createEtherAddress),
    
    #Ether
    path('ether-get/<int:user_id>/', EtherGet.as_view()),
    path('create-ether/', EtherCreate.as_view()),
    #なぜurlパラメータにuser_idを採用したのかわからない
    path('ether-update/<int:user_id>/', EtherUpdate.as_view()),
    #path('ether/<int:user_id>/', EtherRetrieveUpdate.as_view()),
    
    #Question
    path('get-question/<slug:flag>/', QuestionList.as_view()),
    path('get-question/<pk>', QuestionGet.as_view()),
    path('create-question/', QuestionCreate.as_view()),
    path('update-question/<pk>/', QuestionUpdate.as_view()),
    # path('search-question/<slug:flag>', QuestionSearch.as_view()),
    
    #Answer
    path('get-answer/<int:question_id>/', AnswerGet.as_view()),
    path('create-answer/', AnswerCreate.as_view()),
    path('update-answer/<pk>/', AnswerUpdate.as_view()),
    
    #Like
    path('question-like/', views.Questionlike),
    path('answer-like/', views.Answerlike),
    
    #Email
    path('send-email/',views.sendEmail)
]