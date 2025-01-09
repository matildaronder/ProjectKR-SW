# Query Local Knowledge Graph
# Query External Knowledge Graph 
# List good songs (how to know if song recommendations is good?)
# Spotify Search
# Create spotify list. 

import time, os, random
import externalquery, localquery
import spotifyAPI, spotipy, spotifytocsv
import listofsongs
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

speed_values    = ["Slow","Medium","Fast"]
time_values     = ["Morning","Afternoon","Evening","Night"]
speed_range     = {
    (0, 0.25): "Slow",
    (0.26, 0.66): "Medium",
    (0.67, 1): "Fast"
}


def main():
    graph       = localquery.init_graph() # Initial graph from music_data.ttl
    user_time_choice    = int(input("Select a time to base your recomendation on: \n 1. Specify Time \n 2. Current time\n"))

    if(user_time_choice == 0):
        currentTime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        timeOfDay   = spotifytocsv.hour_to_daytime(currentTime)
    else:
        timeOfDay   = choseTimeOfDay()

    user_speed_choice = int(input("Choose what tempo you want to base your playlist on: \n 0. Slow \n 1. Medium \n 2. Fast \n"))
    local_spotify_song_list = localquery.local_query(graph, time_values[timeOfDay]) # Returns 10 spotify songs from user data
    list_len = len(local_spotify_song_list)
    
    collected_list = []
    num_of_retrieved_songs = 25
    for i in range(num_of_retrieved_songs):
        randomInt = random.randint(0, list_len)
        collected_list.append(local_spotify_song_list[randomInt])

    queried_songs_wikidata  = []

    for song,artist in collected_list:
        query_wikidata  = externalquery.wikidata_query(artist, song)
        if query_wikidata: queried_songs_wikidata.extend(query_wikidata)

    # Combine the results
    combined_results = collected_list + queried_songs_wikidata
    
    # The number of random recommended songs
    num_songs = 75
    random_songs = listofsongs.list_of_songs(combined_results, num_songs)

    if(os.getenv('SKIP_SPOTIFY') == "0"):
        sp =spotifyAPI.authenticate()
        user    = sp.current_user()
        user_id = user['id']
        playlist_name = f"Hit-Me: A {speed_values[user_speed_choice]} for the {time_values[timeOfDay]}"
        playlist_id = spotifyAPI.create_playlist(sp,user_id, name = playlist_name)

        track_uris = []
        for track,artist in random_songs:
            track_uri = spotifyAPI.search_track(artist,track,sp)
            if(track_uri):
                track_uris.append(track_uri)

        if(track_uris):
            spotifyAPI.add_tracks_to_playlist(sp,playlist_id,track_uris)
    else:
        print(f"\n{num_songs} Recommended Songs:")
        print("-------------------------------------------------------")
        print(f"Song:{" ":<25}| Artist: ")
        print("-------------------------------------------------------")
        for song, artist in random_songs:
            print(f"{song:<30}| {artist}")

def choseTimeOfDay():
    timeOfDay = int(input("What time of day would you base your music recommendation on? \n 0. Morning \n 1. Afternoon \n 2. Evening \n 3. Night \n"))
    return timeOfDay

if __name__ == "__main__":
    main()