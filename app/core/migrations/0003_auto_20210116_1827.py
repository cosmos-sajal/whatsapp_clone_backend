# Generated by Django 2.2.13 on 2021-01-16 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_thread_threadparticipant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
