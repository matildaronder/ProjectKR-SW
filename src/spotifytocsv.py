import pandas as pd
import json
import os
import glob
from datetime import datetime

directory_path = '../include/SpotifyCSV2/Gustav'

mega_data = []

def hour_to_daytime(time: str):
    dt = datetime.strptime(time, "%Y-%m-%d %H:%M")
    hour = dt.hour
    day_range = {
        range(0, 6): "Night",
        range(6, 12): "Morning",
        range(12, 18): "Afternoon",
        range(18, 24): "Evening"
    }
    for key in day_range:
        if hour in key:
            return day_range[key]
    
def init_spotifyCSV():
    for file_path in glob.glob(os.path.join(directory_path, '*.json')):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        filter_data = []
        for item in data:
            filter_data = {
                'time_of_day': hour_to_daytime(item.get('endTime')),
                'track_name': item.get('trackName'),
                'artist_name': item.get('artistName')
            }
            mega_data.append(filter_data)

    df = pd.DataFrame(mega_data)
    df.drop_duplicates(inplace=True)

    df.to_csv('../data/spotify_values.csv', index=False)
    print("Done creating Spotify Data CSV")