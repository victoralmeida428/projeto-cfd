from django.contrib import admin
from financa.models import BancoUsuarios
# Register your models here.


class ListaUsuarios(admin.ModelAdmin):
    list_display = ("id", "nome", "login", 'email', 'salario', 'nascimento')
    list_display_links = ('id', 'nome')
    search_fields = ('login', 'email')
    list_filter = ('login', 'email')


admin.site.register(BancoUsuarios, ListaUsuarios)
