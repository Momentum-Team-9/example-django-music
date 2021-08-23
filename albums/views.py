from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Album, Genre
from .forms import AlbumForm


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
            album = form.save(commit=False)
            album.save()
            return redirect("show_album", pk=album.pk)
    else:
        form = AlbumForm()

    return render(request, "albums/add_album.html", {"form": form})


@login_required
def show_album(request, pk):
    album = get_object_or_404(Album, pk=pk)
    fav_albums = request.user.fav_albums.all()
    return render(
        request, "albums/show_album.html", {"album": album, "fav_albums": fav_albums}
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
    # if it is, remove favorite
    if user.fav_albums.filter(id=album.id).exists():
        album.favorited_by.remove(user)
    else:
        album.favorited_by.add(user)

    return redirect("show_album", pk=album_pk)

def search(request):
    # what are the query params?
    query = request.GET.get("query")
    # look up that stuff in the db
    # search on album title field only
    # search_results = Album.objects.filter(title__icontains=query)
    # search on album title OR artist name
    search_results = Album.objects.filter(Q(title__icontains=query) | Q(artist__name__icontains=query))
    # pass that stuff that I looked up into the view context

    # return search results (that I've gotten by searching with the search term from query params)
    return render(request, "albums/list_albums.html", {"albums": search_results})
