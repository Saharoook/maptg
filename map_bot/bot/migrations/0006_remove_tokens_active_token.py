# Generated by Django 4.2.4 on 2023-09-01 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_alter_tokens_connected_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tokens',
            name='active_token',
        ),
    ]