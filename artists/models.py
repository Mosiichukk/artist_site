from django.contrib.auth.models import User
from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    photo=models.FileField(upload_to="photos/%Y/%m/%d/",default=True,blank=None,
                            null=True,verbose_name="Фото")
    created_by = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artist', null=True, blank=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=100)
    release_year = models.IntegerField(blank=True, null=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    image_album = models.FileField(upload_to="image_album", default=True, blank=None, null=True, verbose_name="Облога альбома")

    def __str__(self):
        return f"{self.title} by {self.artist.name}"

class Song(models.Model):
    title = models.CharField(max_length=100)
    release_year = models.IntegerField(blank=True, null=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)
    image_song=models.FileField(upload_to="image_song",default=True,blank=None,null=True,verbose_name="Облога пісні")

    def __str__(self):
        return self.title

class Lyrics(models.Model):
    song = models.OneToOneField(Song, on_delete=models.CASCADE)
    lyric_text = models.TextField()

    def __str__(self):
        return f"Lyrics for {self.song.title}"

class Feature(models.Model):
    feature_artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.feature_name} featuring {self.feature_artist.name} in {self.song.title}"

class Audio(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='audio_uploads')
    song = models.OneToOneField(Song, on_delete=models.CASCADE, related_name='audio', null=True, blank=True)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='video/')
    song = models.OneToOneField(Song, on_delete=models.CASCADE, related_name='video', null=True, blank=True)

    def __str__(self):
        return self.title

