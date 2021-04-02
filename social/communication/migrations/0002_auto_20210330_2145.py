# Generated by Django 3.1.7 on 2021-03-30 21:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('communication', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_I_have_received', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='message_sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_I_have_send', to=settings.AUTH_USER_MODEL),
        ),
    ]
