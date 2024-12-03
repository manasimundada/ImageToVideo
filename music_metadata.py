from mutagen.mp3 import MP3

mp3_file_path = 'sus.mp3'
audio = MP3(mp3_file_path)

# Getting the metadata
title = audio.get('title')
artist = audio.get('artist')
album = audio.get('album')
duration_in_seconds = audio.info.length

print(f'Title: {title}')
print(f'Artist: {artist}')
print(f'Album: {album}')
print(f'Duration (seconds): {duration_in_seconds}')
print(audio['TSSE'])