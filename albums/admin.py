from django.contrib import admin
from .models import Album, User

# Register your models here.
admin.site.register(Album)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
