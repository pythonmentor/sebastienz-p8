from django.conf.urls import url
from django.urls import path, re_path

from . import views

app_name = "store"

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('<int:product_id>/substitutes/', views.substitutes, name='substitutes'),
    path('<int:product_id>/', views.details, name='details')
]
