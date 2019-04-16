from django.contrib import admin
from .models import Collection, Interior, Wallpaper


class WallpapersAdmin(admin.ModelAdmin):
    list_display = ('article', 'collection')

admin.site.register(Collection)
admin.site.register(Interior)
admin.site.register(Wallpaper, WallpapersAdmin)

