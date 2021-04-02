# Generated by Django 3.1.7 on 2021-03-30 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dialog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant_one', models.CharField(max_length=100, null=True)),
                ('participant_two', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_time', models.DateTimeField(auto_now_add=True)),
                ('message_content', models.TextField()),
                ('dialog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='communication.dialog')),
            ],
            options={
                'ordering': ('current_time',),
            },
        ),
    ]
