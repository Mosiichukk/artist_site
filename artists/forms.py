from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import request

from .models import Song, Lyrics, Artist, Album, Audio, Video


class AddSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'release_year', 'album', 'image_song']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'album': forms.Select(attrs={'class': 'form-control'}),
            'image_song': forms.FileInput(attrs={'class': 'form-control'}),
        }



class AddLyricsForm(forms.ModelForm):
    class Meta:
        model = Lyrics
        fields = ['lyric_text']
        widgets = {
            'lyric_text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class AddAudioForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ['title','audio_file']

class AddVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title','video_file']
class AddArtistForm(forms.ModelForm):
    class Meta:
        model=Artist


        fields=['name','genre','country','photo']

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'release_year', 'image_album']