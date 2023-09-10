# Generated by Django 4.2.4 on 2023-08-31 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_tokens_admin_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokens',
            name='active_token',
            field=models.BooleanField(blank=True, default=True, verbose_name='Активен ли токен'),
        ),
        migrations.AlterField(
            model_name='tguser',
            name='admin_check',
            field=models.BooleanField(blank=True, default=False, verbose_name='Может ли добавлять точки'),
        ),
        migrations.AlterField(
            model_name='tokens',
            name='admin_check',
            field=models.BooleanField(blank=True, default=False, verbose_name='Админ ли новый пользователь'),
        ),
    ]
