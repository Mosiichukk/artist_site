# Generated by Django 5.0.1 on 2024-05-12 17:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0004_artist_photo_alter_audio_audio_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='song',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video', to='artists.song'),
        ),
    ]
