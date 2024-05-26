from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import generics
from rest_framework.generics import get_object_or_404

import artists.views
from .forms import AddSongForm, AddLyricsForm, AddAudioForm, AddArtistForm, AddVideoForm, RegisterForm, AlbumForm
from .models import *
from .serializers import ArtistSerializer

menu=["Головна","Пошук","Артисти"]
def index(request):
    if request.user.is_authenticated:
        try:
            artist = Artist.objects.get(created_by=request.user.id)
            has_artist = True
            songs = Song.objects.filter(artist=artist)
            albums = Album.objects.filter(artist=artist)
            videos=Video.objects.filter(artist=artist)

        except Artist.DoesNotExist:
            artist = None
            songs=None
            has_artist = False
            albums=None
            videos=None
    else:
        songs = None
        artist = None
        has_artist = False
        albums=None
        videos = None
    return render(request, 'artists/index.html',{'title': 'Головна сторінка', 'menu':menu,'artist':artist,
                                                 'has_artist':has_artist,'songs':songs,'albums':albums,'videos':videos})

def about(request):
    return render(request,'artists/about.html',{'title': 'Про сайт', 'menu':menu})

def all_artists(request):
    artists=Artist.objects.all()
    return render(request,'artists/all_artists.html',{'title': 'Артисти', 'menu':menu, 'artists': artists})

def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    songs = Song.objects.filter(artist=artist)
    albums=Album.objects.filter(artist=artist)
    videos=Video.objects.filter(artist=artist)
    return render(request, 'artists/artist_detail.html', {'title': artist.name, 'menu':menu, 'artist': artist,'songs': songs,'albums':albums,'videos':videos})

def song_detail(request, song_id):
    song = get_object_or_404(Song, pk=song_id)


    lyric_text = get_object_or_404(Lyrics, song=song_id)
    artist = song.artist
    songs = Song.objects.filter(artist=artist)
    audios=None
    playlist = []
    try:
        audio = Audio.objects.get(song=song)
    except Audio.DoesNotExist:
        # Якщо аудіо для пісні не знайдено
        pass

    return render(request, 'artists/song_detail.html', { 'title': song.title,'audio':audio, 'menu':menu, 'lyric_text':lyric_text,'artist':artist,'songs':songs,'song':song})
def video_detail(request, video_id):
    video=None
    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        # Якщо аудіо для пісні не знайдено
        pass
    song=video.song
    artist = video.artist

    return render(request, 'artists/video.html', { 'title': video.title,'video':video, 'menu':menu, 'artist':artist,'song':song})

def album_detail(request, album_id,num_song):
    album = get_object_or_404(Album, pk=album_id)
    songs=Song.objects.filter(album_id=album_id)
    lyrics=[]
    audios=[]
    for s in songs:
        l=get_object_or_404(Lyrics,song=s.id)
        a=get_object_or_404(Audio,song=s.id)
        lyrics.append(l)
        audios.append(a)

    return render(request, 'artists/album_detail.html', {'album': album,'title': album.title, 'menu':menu,'songs':songs,'lyrics':lyrics,'audios':audios,'num_song':num_song})

def search(request):
    query = request.GET.get('q', '').lower()
    artist_query, song_query = query, query


    if '-' in query:
        parts = query.split('-')
        if len(parts) == 2:
            artist_query, song_query = parts[0].strip(), parts[1].strip()

    # Фільтруйте артистів і пісні за відповідними запитами
    artists = Artist.objects.filter(name__icontains=artist_query)
    songs = Song.objects.filter(title__icontains=song_query)


    return render(request, 'artists/search_results.html', {'query': query, 'songs': songs, 'artists': artists, 'title':query})

def add_information_song(request):
    try:
        artist = Artist.objects.get(created_by=request.user)
    except Artist.DoesNotExist:
        artist = None

    if request.method == 'POST':
        form = AddSongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            if artist:
                song.artist = artist
                song.save()
                return redirect('add_lyrics', song_id=song.id)  # Перенаправлення після успішного збереження
            else:
                form.add_error(None, "Ви повинні спочатку створити акаунт артиста.")
    else:
        form = AddSongForm()

    data={

        'menu': menu,
        'title': 'Додавання сторінки:',
        'form':  form

    }
    return render(request, 'artists/add_information.html', data)
def add_information_lyrics(request,song_id):
    song = get_object_or_404(Song, id=song_id)

    if request.method == 'POST':
        form = AddLyricsForm(request.POST)
        if form.is_valid():
            lyrics = form.save(commit=False)
            lyrics.song = song
            lyrics.save()
            return redirect('add_audio', song_id=song.id)
    else:
        form = AddLyricsForm()

    data={

        'menu': menu,
        'title': 'Додавання тексту:',
        'form':  form

    }
    return render(request, 'artists/add_information.html', data)
def add_information_artist(request):
    if Artist.objects.filter(created_by=request.user).exists():
        return redirect('index')
    error_message = None
    if request.method == 'POST':
        form = AddArtistForm(request.POST, request.FILES)
        form.created_by = request.user


        if form.is_valid():
            img_file = form.cleaned_data['photo']
            if not img_file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):  # Перевірка розширення файла
                error_message = "*Непідтримуваний формат зображення"
            else:
                form.save()
                artist = form.save(commit=False)
                artist.created_by = request.user
                artist.save()
                return redirect('index')
        else:
            error_message = "*Неправильний формат зображення"


    else:
        form = AddArtistForm()
        form.created_by = request.user

    data = {

        'menu': menu,
        'title': 'Додавання Артиста:',
        'form': form,
        'error_message': error_message

    }
    return render(request, 'artists/add_information.html', data)

def add_information_audio(request,song_id):

    error_message=None
    song = get_object_or_404(Song, id=song_id)
    artist = get_object_or_404(Artist, created_by=request.user)

    if request.method== 'POST':
        form = AddAudioForm(request.POST, request.FILES)

        if form.is_valid():
            audio_file = form.cleaned_data['audio_file']
            if not audio_file.name.endswith(('.mp3', '.wav', '.ogg')):  # Перевірка розширення файла
                error_message = "*Непідтримуваний формат аудіо"
            else:
                audio = form.save(commit=False)
                audio.song = song
                audio.artist = artist
                audio.save()

                return redirect('index')
        else:
            error_message = "*Неправильний формат аудіо"


    else:
        form=AddAudioForm()

    data={

        'menu': menu,
        'title': 'Додавання аудіо:',
        'form':  form,
        'error_message': error_message

    }
    return render(request, 'artists/add_information.html', data)


def add_information_album(request):
    try:
        artist = Artist.objects.get(created_by=request.user)
    except Artist.DoesNotExist:
        artist = None

    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False)
            if artist:
                album.artist = artist
                album.save()
                return redirect('index')  # Перенаправлення на сторінку списку альбомів
            else:
                form.add_error(None, "Ви повинні спочатку створити акаунт артиста.")
    else:
        form = AlbumForm()

    data = {
        'form': form,
        'title': 'Додавання альбому:'
    }
    return render(request, 'artists/add_information.html', data)
# Create your views here.
class ArtistAPIView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')  # Перенаправлення на головну сторінку після входу
    else:
        form = AuthenticationForm()
    return render(request, 'artists/add_information.html', {'form': form})

def add_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('album_list')  # Перенаправлення на сторінку списку альбомів
    else:
        form = AlbumForm()
    return render(request, 'add_album.html', {'form': form})

def add_information_video(request, song_id):
    error_message = None
    song = get_object_or_404(Song, id=song_id)
    artist = get_object_or_404(Artist, created_by=request.user)

    if request.method == 'POST':
        form = AddVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = form.cleaned_data['video_file']
            if not video_file.name.endswith(('.mp4', '.avi', '.mov')):  # Перевірка розширення файла
                error_message = "*Непідтримуваний формат відео"
            else:
                video = form.save(commit=False)
                video.song = song
                video.artist = artist
                video.save()
                return redirect('index')
        else:
            error_message = "*Неправильний формат відео"

    else:
        form = AddVideoForm()

    data = {
        'menu': menu,
        'title': 'Додавання відео:',
        'form': form,
        'error_message': error_message
    }
    return render(request, 'artists/add_information.html', data)
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Перенаправлення на головну сторінку після реєстрації
    else:
        form = RegisterForm()
    return render(request, 'artists/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')