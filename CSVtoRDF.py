import csv
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS
from urllib.parse import quote

g = Graph()
MUSIC = Namespace("http://purl.org/ontology/mo/")

def sanitize_for_uri(value):
    return quote(value.replace(" ", "_").replace('"', "").replace("(", "").replace(")", "").replace(",", ""))


with open("./Project/spotify_values.csv", "r", encoding='utf-8') as file:
    reader = csv.reader(file, quotechar='"', delimiter=',')

    next(reader)

    for row in reader:
        time_of_day, track_name, artist_name = row
        sanitized_artist_name = sanitize_for_uri(artist_name)
        sanitized_track_name = sanitize_for_uri(track_name)
        artist_uri = URIRef(MUSIC[sanitized_artist_name])
        track_uri = URIRef(MUSIC[sanitized_track_name])

        # Adding Artist
        g.add((artist_uri, RDF.type, MUSIC.MusicArtist))
        g.add((artist_uri, RDFS.label, Literal(artist_name)))

        # Adding Album, Can be added if using SpotifyCSV

        #sanitized_album_name = sanitize_for_uri(album_name)
        #album_uri = URIRef(MUSIC[sanitized_album_name])
        #g.add((album_uri, RDF.type, MUSIC.Album))
        #g.add((album_uri, RDFS.label, Literal(album_name)))
        #g.add((album_uri, MUSIC.producer, artist_uri))
        #g.add((track_uri, MUSIC.published_as, album_uri)) 

        # Adding Track
        g.add((track_uri, RDF.type, MUSIC.Track))
        g.add((track_uri, RDFS.label, Literal(track_name)))
        g.add((track_uri, MUSIC.performer, artist_uri))
        g.add((track_uri, MUSIC.time, Literal(time_of_day)))

g.serialize("music_data.ttl", format="turtle")
print("Done")