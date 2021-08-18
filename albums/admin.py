from django.contrib import admin
from .models import Album, User, Genre

# Register your models here.
admin.site.register(Album)
admin.site.register(Genre)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
