# Generated by Django 4.1 on 2022-12-07 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_comentario_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='setor',
            name='ocupacoes',
            field=models.ManyToManyField(to='api.ocupacao'),
        ),
    ]
