from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('link/', views.link, name='link'),
    path('compare/', views.compare, name='compare'),
    path('conditions/', views.conditions, name='conditions')
]