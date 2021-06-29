from django.contrib import admin
from .models import Album, User, Artist, PlayList

# Register your models here.
admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(PlayList)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
