from django.urls import path
from . import views

app_name = 'library_rpc'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.jsonrpc_handler, name='jsonrpc'),
    path('reset-data/', views.reset_data, name='reset_data'),
]
