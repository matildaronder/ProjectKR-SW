import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

def authenticate():
    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    #Registered Redirect URI
    REDIRECT_URI = os.getenv("REDIRECT_URI")

    #Spotify API
    SCOPE = 'playlist-modify-private'
    sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id = CLIENT_ID,
                                               client_secret = CLIENT_SECRET,
                                               redirect_uri = REDIRECT_URI,
                                               scope=SCOPE))
    return sp

def create_playlist(sp,user_id, name = "My Playlist", description = "Created by Dream team group 5"):
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