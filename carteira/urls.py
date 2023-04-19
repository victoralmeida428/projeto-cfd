from django.urls import path
from carteira.views import dash, balanco

urlpatterns = [
    path('dash', dash, name='dash'),
    path('balanco', balanco, name='balanco')

]
