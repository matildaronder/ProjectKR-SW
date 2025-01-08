import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

from SPARQLWrapper import SPARQLWrapper, JSON

# Define the SPARQL endpoint for Wikidata
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setReturnFormat(JSON)

# Define the SPARQL query
query = """
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?song ?songLabel ?artist ?artistLabel ?bpm WHERE {
        ?song wdt:P31 wd:Q7366 ;
            wdt:P175 ?artist ;
            wdt:P1725 ?bpm .

        SERVICE wikibase:label {
        bd:serviceParam wikibase:language "en" .
        ?song rdfs:label ?songLabel .
        ?artist rdfs:label ?artistLabel .
        }
    }
    LIMIT 10
    """
sparql.setQuery(query)

# Execute the query
results = sparql.queryAndConvert()

# Print results
for result in results["results"]["bindings"]:
    print(f"Song: {result['songLabel']['value']}, Artist: {result['artistLabel']['value']}, BPM: {result['bpm']['value']}")

def authenticate():
    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
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