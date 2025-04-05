from django.urls import path
from . import views

# Název aplikace pro namespacing URL
app_name = 'birthday'

# Definice URL vzorů pro aplikaci
urlpatterns = [
    # Hlavní stránka se seznamem narozenin
    path('', views.birthday_list, name='birthday_list'),
    # URL pro smazání konkrétních narozenin podle ID
    path('delete/<int:birthday_id>/', views.delete_birthday, name='delete_birthday'),
    path('test-mail/', views.test_birthday_email, name='test_email'),

]
