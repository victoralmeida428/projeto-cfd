from django.db import models
import datetime as dt

class ContaUsuario(models.Model):

    login = models.CharField(max_length=50, blank=False, editable=False)
    valor = models.DecimalField(decimal_places=2, editable=True,
                                  max_digits=100, default=0.00, blank=False)
    categoria = models.CharField(max_length=100, blank=False)
   
    extra_gasto = models.CharField(max_length=100, blank=True, null=True)
    data = models.DateField(default='')
