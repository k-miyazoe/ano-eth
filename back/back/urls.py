from django.contrib import admin
from django.urls import path,include
from rest_framework_jwt.views import obtain_jwt_token



urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', obtain_jwt_token), 
    #path('app/', include('app.urls')),
]
