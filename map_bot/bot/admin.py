from django.contrib import admin
from .models import TgUser, Point, Tokens


admin.site.register(TgUser)
admin.site.register(Point)
admin.site.register(Tokens)

