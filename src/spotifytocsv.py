import pandas as pd
import json
import os
import glob
from datetime import datetime

directory_path = './include/SpotifyCSV2/Gustav'
spotify_tracks_path = './data/tracks_features.csv'


def classify_bpm(bpm):

    if(bpm):
        bpm = float(bpm)
        if bpm <= 90:
            return "Low"
        elif 91 <= bpm <= 140:
            return "Medium"
        else:
            return "High"
    else:
        print(bpm)
    
def createPandaCSV(csvPath):
    dataframe = pd.read_csv(csvPath)
    return dataframe

def queryPandaBPM(dataframe, song):
    filtered = dataframe[dataframe['name'] == f"{song}"]
    if not(filtered['tempo'].isna().all()):
        return filtered['tempo'].iloc[0]
    else:
        return 120



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
    dataframe = createPandaCSV(spotify_tracks_path)
    mega_data = []
    # Assuming 'dataframe' is your DataFrame
    for file_path in glob.glob(os.path.join(directory_path, '*.json')):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        filter_data = []
        for iteration, item in enumerate(data):
            filter_data = {
                'time_of_day': hour_to_daytime(item.get('endTime')),
                'track_name': item.get('trackName'),
                'artist_name': item.get('artistName'),
                'bpm'       : classify_bpm(queryPandaBPM(dataframe,item.get('trackName')))
            }
            print(f"{iteration} out of {len(data)} {len(data)-iteration} is left")
            mega_data.append(filter_data)
        
    df = pd.DataFrame(mega_data)
    df.drop_duplicates(inplace=True)

    df.to_csv('./data/spotify_values2.csv', index=False)
    print("Done creating Spotify Data CSV")
    


