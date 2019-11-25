from django.conf.urls import url
from django.urls import path, re_path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.user_login, name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('myaccount/', views.user_account, name='myaccount'),
]
