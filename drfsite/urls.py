"""
URL configuration for drfsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import logout
from django.shortcuts import redirect

from artists import views
from artists.views import ArtistAPIView, index, about, all_artists, artist_detail, album_detail, song_detail, search, \
    add_information_song, add_information_lyrics, add_information_audio, add_information_artist, \
    video_detail, add_information_album, add_information_video
from drfsite import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/artistlist/', ArtistAPIView.as_view()),
    path('', index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('about/',about,name='about'),
    path('artists/',all_artists,name='all_artists'),
    path('artists/<int:artist_id>/', artist_detail, name='artist_detail'),
    path('song/<int:song_id>/', song_detail, name='song_detail'),
    path('video/<int:video_id>/',video_detail, name='video_detail'),
    path('album/<int:album_id>/<int:num_song>/', album_detail, name='album_detail'),
    path('search/', search, name='search'),
    path('add/informationsong/',add_information_song, name='add_song'),
    path('add/lyrics/<int:song_id>/', add_information_lyrics,name='add_lyrics'),
    path('add/audio/<int:song_id>/',add_information_audio,name="add_audio"),
    path('add/artist/',add_information_artist, name='add_artist'),
    path('add/video/<int:song_id>/',add_information_video, name='add_video'),
    path('add/album',add_information_album,name='add_album')


]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
