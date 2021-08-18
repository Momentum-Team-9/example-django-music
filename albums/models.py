from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return self.username

class Genre(models.Model):
    name = models.CharField(max_length=75)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Genre name={self.name}>"

class Album(models.Model):
    title = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    genres = models.ManyToManyField(Genre, related_name="albums")

    def __repr__(self):
        return f"<Album title={self.title} artist_name={self.artist_name}>"

    def __str__(self):
        return self.title

