from django.contrib import admin
from userprofiles.models import *

class VideoAdmin(admin.ModelAdmin):
    # define which columns displayed in changelist
    list_display = ('id', 'title', 'id_user', 'date', 'views', 'searched', 'likes',)
    list_filter = ('id', 'title', 'id_user', 'date',)

class NewAdmin(admin.ModelAdmin):
    # define which columns displayed in changelist
    list_display = ('id', 'alert', 'id_user', 'date', 'sumary',)
    list_filter = ('id', 'alert', 'id_user', 'date',)
# Register your models here.
admin.site.register(New)
admin.site.register(Video, VideoAdmin)