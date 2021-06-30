from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q

from .models import Album, Genre, PlayList
from .forms import AlbumForm
from .utils import is_ajax


def homepage(request):
    # show a homepage
    if request.user.is_authenticated:
        return redirect("list_albums")
    return render(request, "albums/homepage.html")


@login_required  # this is a decorator or function that will redirect you to login page
def list_albums(request):
    albums = Album.objects.all().order_by("title")
    return render(request, "albums/list_albums.html", {"albums": albums})


@login_required
def add_album(request):
    if request.method == "POST":
        form = AlbumForm(data=request.POST)
        if form.is_valid():
            album = form.save()
            return redirect("show_album", pk=album.pk)
    else:
        form = AlbumForm()

    return render(request, "albums/add_album.html", {"form": form})


@login_required
def show_album(request, pk):
    album = get_object_or_404(Album, pk=pk)
    favorited = request.user.fav_albums.filter(id=album.id).exists()
    return render(
        request, "albums/show_album.html", {"album": album, "favorited": favorited}
    )


@login_required
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


@login_required
def delete_album(request, pk):
    album = get_object_or_404(Album, pk=pk)

    if request.method == "POST":
        album.delete()
        messages.success(request, "Album deleted.")
        return redirect("list_albums")

    return render(request, "albums/delete_album.html", {"album": album})


@login_required
def show_genre(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    albums = genre.albums.all()

    return render(request, "albums/show_genre.html", {"genre": genre, "albums": albums})


@login_required
def toggle_favorite(request, album_pk):
    # get the user
    user = request.user
    # get the album
    album = get_object_or_404(Album, pk=album_pk)
    # check to see if album is already favorited by user
    if user.fav_albums.filter(id=album.id).exists():
        # if it is, remove favorite
        print("Ok, unfavorited!")
        favorited = False
        album.favorited_by.remove(user)
    else:
        print("Ok, favorited!")
        favorited = True
        album.favorited_by.add(user)

    if is_ajax(request):
        # response with Json that says request succeeded and whether this album is favorited or not
        return JsonResponse({"favorited": favorited}, status=200)

    return redirect("show_album", pk=album_pk)


def search(request):
    query = request.GET.get("q")
    results = Album.objects.filter(
        Q(title__icontains=query) | Q(artist__name__icontains=query)
    )

    return render(request, "albums/list_albums.html", {"albums": results})


@login_required
def add_to_playlist(request, playlist_pk):
    playlist = PlayList.objects.get(pk=playlist_pk)

    # check if current user owns playlist
    if request.user is not playlist.owner:
        print("Unauthorized!")
        messages.add_message(
            request, messages.ERROR, "Only the owner can add to this playlist"
        )
        return redirect("list_albums")

    # If I make this a GET I can use a query param "album=some+album+title"
    album_title = request.GET.get("album")
    album = Album.objects.filter(title__iexact=album_title)
    playlist.albums.add(album)
    messages.add_message(
        request, messages.SUCCESS, "Album has been added to your playlist"
    )

    return redirect("show_album")
