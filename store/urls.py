from django.conf.urls import url
from django.urls import path, re_path

from . import views

app_name = "store"

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('<int:product_id>/substitutes/', views.substitutes, name='substitutes'),
    path('<int:product_id>/', views.details, name='details'),
    path('<int:product_id>/<int:substitute_id>/', views.save_substitute, name='save_substitute'),
    path('favorites/', views.favorites_substitutes, name='favorites_substitutes'),
    path('favorites/<int:product_id>/<int:substitute_id>/', views.delete_favorite, name='delete_favorite'),
    path('mentions_legal/', views.mentions_legal, name='mentions_legal'),
]
