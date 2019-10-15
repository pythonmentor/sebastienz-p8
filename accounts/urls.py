from django.conf.urls import url
from . import views

app_name = "accounts"

urlpatterns = [
    url(r'^$', views.user_login, name='login'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^register/$', views.user_register, name='register')
]
