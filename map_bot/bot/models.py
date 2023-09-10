from django.db import models


class TgUser(models.Model):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    nick_name = models.CharField(max_length=200,
                                 blank=True,
                                 verbose_name='Никнейм в телеграм')

    tg_id = models.PositiveIntegerField(default=0,
                                        blank=True,
                                        verbose_name='ID пользователя в телеграм'
                                        )

    admin_check = models.BooleanField(default=False,
                                      blank=True,
                                      verbose_name='Может ли добавлять точки')

    def __str__(self):
        return self.nick_name


class Point(models.Model):

    class Meta:
        verbose_name = 'Точка'
        verbose_name_plural = 'Точки'

    latitude = models.FloatField()
    longitude = models.FloatField()

    name = models.CharField(max_length=200,
                            blank=True,
                            verbose_name='Название места')

    description = models.TextField(blank=True,
                                   verbose_name='Описание места')

    navigator_link = models.URLField(blank=True,
                                     max_length=1000,
                                     verbose_name='Ссылка на навигатор')

    def __str__(self):
        return self.name


class Tokens(models.Model):

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'

    creation_time = models.DateTimeField(auto_now_add=True,
                                         verbose_name='Время создания токена')

    token_creator = models.ForeignKey(TgUser, on_delete=models.SET_NULL, null=True,
                                      verbose_name='Создатель токена', related_name='token_creator')

    token = models.CharField(max_length=25, verbose_name='Токен')

    admin_check = models.BooleanField(default=False,
                                      blank=True,
                                      verbose_name='Админ ли новый пользователь')

    joined_user = models.ForeignKey(TgUser, on_delete=models.SET_NULL, blank=True, null=True,
                                    verbose_name='Присоединившийся пользователь', related_name='joined_user')

    activated = models.BooleanField(default=False,
                                    blank=False,
                                    verbose_name='Был ли токен использован')

    def __str__(self):
        return self.token_creator.nick_name



