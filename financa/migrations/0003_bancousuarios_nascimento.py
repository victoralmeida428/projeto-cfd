# Generated by Django 4.2 on 2023-04-15 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financa', '0002_bancousuarios_salario'),
    ]

    operations = [
        migrations.AddField(
            model_name='bancousuarios',
            name='nascimento',
            field=models.DateField(default='1900-1-2'),
        ),
    ]
