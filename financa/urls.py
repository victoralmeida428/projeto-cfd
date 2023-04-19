from django.urls import path
from financa.views import (login, cadastro, about,
                           index, logout, cadastro_efetuado)

urlpatterns = [
    path('', index, name='index'),
    path('login', login, name='login'),
    path('cadastro', cadastro, name='cadastro'),
    path('cadastro_efetuado', cadastro_efetuado, name='cadastro_efetuado'),
    path('about', about, name='about'),
    path('logout', logout, name='logout')
]
