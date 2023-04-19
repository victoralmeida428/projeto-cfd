from django.contrib import admin
from carteira.models import ContaUsuario
# Register your models here.

class ContasUsuarios(admin.ModelAdmin):
    list_display = ("id", "login", 'valor', 'categoria')
    list_display_links = ('id', 'login',)
    search_fields = ('login', )
    


admin.site.register(ContaUsuario, ContasUsuarios)