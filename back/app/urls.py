from django.urls import path
from .views import *

name="app"

urlpatterns = [
    path('users/', UserList.as_view()),
    path('create-user/',UserCreate.as_view()),
    path('users/<pk>/', UserRetrieveUpdate.as_view()),
]
