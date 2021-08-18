from django import forms
from .models import Album, Genre


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ["title", "artist_name", "genres"]
        