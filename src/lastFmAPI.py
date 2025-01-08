import requests,os

BASE_URL    = "http://ws.audioscrobbler.com/2.0/"
API_KEY     = os.getenv('LAST_FM_ID')

# Function to fetch track info
def get_track_info(artist, track):
    params = {
        'method': 'track.getinfo',  # API method for track info
        'api_key': 'b2bfff88730149526107c59dd2a4e1b7',
        'artist': artist,
        'track': track,
        'format': 'json'  # Response format
    }

    try:
        print(params)
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        # Print track info
        if 'track' in data:
            track_info = data['track']
            print(f"Track: {track_info['name']}")
            print(f"Artist: {track_info['artist']['name']}")
            print(f"Album: {track_info.get('album', {}).get('title', 'N/A')}")
            print(f"Listeners: {track_info['listeners']}")
            print(f"Playcount: {track_info['playcount']}")
            print(f"toptags: {track_info['toptags']}")
            print(f"streamability:{track_info['streamable']}")
            print(f"duration:{track_info['duration']}")
        else:
            print("Track not found or missing data.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage
get_track_info("Coldplay", "Yellow")