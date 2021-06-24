from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import Album, Genre
from .forms import AlbumForm


def homepage(request):
    # show a homepage
    return render(request, "albums/homepage.html")


@login_required # this is a decorator or function that will redirect you to login page
def list_albums(request):
    albums = Album.objects.all().order_by("title")
    return render(request, "albums/list_albums.html", {"albums": albums})


def add_album(request):
    if request.method == "POST":
        form = AlbumForm(data=request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.save()
            return redirect("show_album", pk=album.pk)
    else:
        form = AlbumForm()

    return render(request, "albums/add_album.html", {"form": form})


def show_album(request, pk):
    album = get_object_or_404(Album, pk=pk)
    return render(request, "albums/show_album.html", {"album": album})


def edit_album(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == "GET":
        form = AlbumForm(instance=album)
    else:
        form = AlbumForm(data=request.POST, instance=album)
        if form.is_valid():
            form.save()
            return redirect("list_albums")

    return render(request, "albums/edit_album.html", {"form": form, "album": album})


def delete_album(request, pk):
    album = get_object_or_404(Album, pk=pk)

    if request.method == "POST":
        album.delete()
        messages.success(request, "Album deleted.")
        return redirect("list_albums")

    return render(request, "albums/delete_album.html", {"album": album})


def show_genre(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    albums = genre.albums.all()

    return render(request, "albums/show_genre.html", {"genre": genre, "albums": albums})


# This view should be login_required
def toggle_favorite(request, album_pk):
    # get the user
    user = request.user
    # get the album
    album = get_object_or_404(Album, pk=album_pk)
    # check to see if album is already favorited by user
    # if it is, remove favorite
    if user.fav_albums.filter(id=album.id).exists():
        album.favorited_by.remove(user)
    else:
        album.favorited_by.add(user)

    return redirect("show_album", pk=album_pk)
