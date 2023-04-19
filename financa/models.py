from django.db import models

class BancoUsuarios(models.Model):
    nome = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=150, blank=False)
    login = models.CharField(max_length=15, blank=False)
    senha = models.CharField(max_length=30 ,blank=False)
    senha_rep = models.CharField(max_length=50, blank=False)
    salario = models.DecimalField(decimal_places=2, editable=True, 
                                  max_digits=100, default=0.00)
    nascimento = models.DateField(default='1900-1-2')
