from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return self.username


class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(
        "Artist", on_delete=models.CASCADE, related_name="albums"
    )
    genres = models.ManyToManyField("Genre", related_name="albums")
    created_at = models.DateTimeField(auto_now_add=True)
    favorited_by = models.ManyToManyField("User", related_name="fav_albums")

    def __repr__(self):
        return f"<Album title={self.title}>"

    def __str__(self):
        return self.title


class Artist(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return f"<Artist name={self.name}>"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=75)

    def __repr__(self):
        return f"<Genre name={self.name}>"

    def __str__(self):
        return self.name


class PlayList(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    albums = models.ManyToManyField(Album)

    def __repr__(self):
        return f"<PlayList name={self.name} owner_id={self.owner.id}>"

    def __str__(self):
        return self.name
