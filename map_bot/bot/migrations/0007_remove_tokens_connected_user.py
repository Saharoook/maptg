# Generated by Django 4.2.4 on 2023-09-01 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_remove_tokens_active_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tokens',
            name='connected_user',
        ),
    ]