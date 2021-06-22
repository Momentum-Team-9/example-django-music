from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return self.username


class Album(models.Model):
    title = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return f"<Album title={self.title} artist_name={self.artist_name}>"

    def __str__(self):
        return self.title


class Artist(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return f"<Artist name={self.name}>"

    def __str__(self):
        return self.name
