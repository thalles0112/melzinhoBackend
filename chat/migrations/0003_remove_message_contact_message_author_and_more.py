# Generated by Django 4.1 on 2022-12-07 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_comentario_time'),
        ('chat', '0002_alter_chat_participants_alter_message_contact_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='contact',
        ),
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='message_author', to='api.userprofile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver', to='api.userprofile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='sec_id',
            field=models.CharField(blank=True, max_length=5000, unique=True),
        ),
    ]