from django.contrib import admin
from .models import Album, User, Artist

# Register your models here.
admin.site.register(Album)
admin.site.register(Artist)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
