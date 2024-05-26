from django.contrib import admin

from .models import Artist, Song, Album, Lyrics, Feature

# Register your models here.
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(Album)
admin.site.register(Lyrics)
admin.site.register(Feature)