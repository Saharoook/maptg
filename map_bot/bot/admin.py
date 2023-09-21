from django.contrib import admin
from .models import TgUser, Point, Tokens, PlacePhoto


admin.site.register(TgUser)
admin.site.register(Point)
admin.site.register(Tokens)
admin.site.register(PlacePhoto)

