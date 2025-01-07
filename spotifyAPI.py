import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

#Spotify API credentials





def authenticate():
    load_dotenv()
    CLIENT_ID = "9c1ab41b9fa64329961895ff2bdb618b"
    CLIENT_SECRET = "bb305798bd5149d28de56c1f64cca720"
    #Registered Redirect URI
    REDIRECT_URI = 'http://localhost:8080/callback/'

    #Spotify API
    SCOPE = 'playlist-modify-private'
    sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id = CLIENT_ID,
                                               client_secret = CLIENT_SECRET,
                                               redirect_uri = REDIRECT_URI,
                                               scope=SCOPE))
    return sp

def create_playlist(sp,user_id, name = "My Playlist", description = "Created by a Python Script"):
    playlist = sp.user_playlist_create(user = user_id, name = name, public = False, description = description)
    return playlist['id']

def add_tracks_to_playlist(sp,playlist_id, track_uris):
    sp.playlist_add_items(playlist_id, track_uris)

def search_track(artist, track,sp):
    query = f"track:{track} artist:{artist}"
    results = sp.search(q = query, type = "track", limit = 1)
    if results['tracks']['items']:
        return results['tracks']['items'][0]['uri']
    else:
        print(f"Track '{track}' by '{artist}' not found.")
        return None

def main():
    user = sp.current_user()
    user_id = user['id']
    print(f"Authenticated as {user['display_name']} (ID: {user_id})")

    playlist_name = "Python Playlist"
    playlist_id = create_playlist(user_id, name = playlist_name)
    print(f"Playlist '{playlist_name}' created successfully! Playlist ID: {playlist_id}")

    #Test
    song_list = [
        ("Miles Davis", "So What"),
        ("The Beatles", "Hey Jude"),
        ("Rihanna", "SOS"),
        ("Adele", "Hello"),
        ("Ed Sheeran", "Shape of You"),
        ("Drake", "God's Plan"),
        ("Taylor Swift", "Shake It Off"),
        ("Billie Eilish", "Bad Guy"),
        ("Post Malone", "Circles"),
        ("Kendrick Lamar", "HUMBLE."),
        ("Beyoncé", "Single Ladies"),
        ("Justin Bieber", "Sorry"),
        ("Shakira", "Hips Don't Lie"),
        ("Elton John", "Rocket Man"),
        ("Queen", "Bohemian Rhapsody"),
        ("Michael Jackson", "Billie Jean"),
        ("Sia", "Chandelier"),
        ("Lady Gaga", "Bad Romance"),
        ("The Weeknd", "Blinding Lights"),
        ("Travis Scott", "SICKO MODE")
    ]
    
    track_uris = []
    
    for artist, track in song_list:
        track_uri = search_track(artist, track)
        if track_uri:
            track_uris.append(track_uri)
    
    if track_uris:
        add_tracks_to_playlist(playlist_id, track_uris)
        print(f"{len(track_uris)} tracks added to the playlist!")
    else:
        print("No tracks were found or added.")

