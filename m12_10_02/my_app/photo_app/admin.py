from django.contrib import admin
from .models import Picture
# Register your models here.


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ['description', 'path', 'get_user_fullname']
    list_filter = ['description', 'user']
    search_fields = ['description', 'path']
    ordering = ['description']

    def get_user_fullname(self, instance):
        if instance.user is not None:
            return instance.user.first_name + ' ' + instance.user.last_name
        else:
            return 'No user'

    get_user_fullname.short_description = 'User'
    