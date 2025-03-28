from django.urls import path
from . import views

app_name = 'crossroad'

urlpatterns = [
    path('', views.index, name='index'),
]
