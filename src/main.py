# Query Local Knowledge Graph
# Query External Knowledge Graph 
# List good songs (how to know if song recommendations is good?)
# Spotify Search
# Create spotify list. 

import time, os
import externalquery, localquery
import spotifyAPI, spotipy, spotifytocsv
import listofsongs
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SKIP_SPOTIFY = os.getenv('SKIP_SPOTIFY')
SCOPE = 'playlist-modify-private'
sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id = CLIENT_ID,
                                            client_secret = CLIENT_SECRET,
                                            redirect_uri = REDIRECT_URI,
                                            scope=SCOPE))

def main():
    graph       = localquery.init_graph() # Initial graph from music_data.ttl
    #user_choice = input(int("1. Specify Time \n 2. Current time"))
    user_choice = 0
    if(user_choice == 0):
        currentTime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        timeOfDay   = spotifytocsv.hour_to_daytime(currentTime)
    else:
        timeOfDay   = choseTimeOfDay()
    spotify_graph   = localquery.local_query(graph,timeOfDay) # Returns 10 spotify songs from user data

    queried_songs_dbpedia   = []
    queried_songs_wikidata  = []
    for song,artist in spotify_graph:
        queried_songs_dbpedia.extend(externalquery.dbpedia_query(artist))
        # queried_songs_wikidata.extend(externalquery.wikidata_query(artist))

    # Combine the results
    combined_results = queried_songs_dbpedia + queried_songs_wikidata
    
    # Select 25 random songs
    random_songs = listofsongs.list_of_songs(combined_results, 25)

        
    collected_list = spotify_graph
    collected_list.extend(queried_songs_dbpedia)

    if(SKIP_SPOTIFY == "0"):
        #Create Spotify playlist
        user    = sp.current_user()
        user_id = user['id']
        playlist_name = "Python Playlist by Gurr and Jac"
        playlist_id = spotifyAPI.create_playlist(sp,user_id, name = playlist_name)

        track_uris = []
        for track,artist in collected_list:
            track_uri = spotifyAPI.search_track(artist,track,sp)
            if(track_uri):
                track_uris.append(track_uri)
        print(track_uris)

        if(track_uris):
            spotifyAPI.add_tracks_to_playlist(sp,playlist_id,track_uris)
    else:
        #print(collected_list)
        print("\n25 Recommended Songs:")
        print("-------------------------------------------------------")
        print(f"Song:{" ":<25}| Artist: ")
        print("-------------------------------------------------------")
        for song, artist in random_songs:
            print(f"{song:<30}| {artist}")


def choseTimeOfDay():
    timeOfDay = input("What time of day would you base your music recommendation on? \n 1. Morning \n 2. Afternoon \n 3. Evening \n 4. Night ")
    return timeOfDay


if __name__ == "__main__":
    main()
