# Generated by Django 4.1 on 2022-11-04 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
    ]