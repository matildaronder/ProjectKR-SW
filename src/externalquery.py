from SPARQLWrapper import SPARQLWrapper, JSON
import re

def dbpedia_query(artistName : str):
    #connect to the DBpedia SPARQL endpoint
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    prefix = """PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX dct: <http://purl.org/dc/terms/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                """

    query_dbpedia = prefix + f"""SELECT ?song ?songLabel ?artist ?artistLabel WHERE {{
                                ?song a dbo:Song ;
                                        dbo:artist ?artist ;
                                        rdfs:label ?songLabel .
                                    ?artist rdfs:label ?artistLabel .
                                FILTER (lang(?songLabel) = "en" && lang(?artistLabel) = "en")
                                FILTER (CONTAINS(?artistLabel, "{artistName}"))
                                }} LIMIT 10"""
    
    sparql.setQuery(query_dbpedia)

    try:
        result = sparql.queryAndConvert()
        results_list = []

        for row in result["results"]["bindings"]:
            song_label = clean_label(row["artistLabel"]["value"])
            artist_label = clean_label(row["songLabel"]["value"])
            results_list.append((artist_label, song_label))
            
    except Exception as e:
        print(e)

    return results_list


def wikidata_query(artistName : str, songName : str):
    #connect to the Wikidata SPARQL endpoint
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    # Check https://www.wikidata.org/wiki/Wikidata:Main_Page for finding P31, and Q7366
    query_wikidata = f"""SELECT DISTINCT ?influencedArtist ?influencedSong ?sameGenreSong ?sameGenreArtistLabel ?recommendedSongLabel ?recommendedArtistLabel
                        WHERE {{
                            ?song rdfs:label "{songName}"@en ;
                                wdt:P175 ?artist .
                            ?artist rdfs:label "{artistName}"@en .

                            OPTIONAL {{
                                ?artist wdt:P737 ?influencedArtist .
                                ?influencedArtist rdfs:label ?recommendedArtistLabel .
                                ?influencedSong wdt:P175 ?influencedArtist ;
                                                wdt:P31/wdt:P279* wd:Q7366 ;
                                                rdfs:label ?recommendedSongLabel .
                                FILTER (lang(?recommendedArtistLabel) = "en" && lang(?recommendedSongLabel) = "en")
                            }}

                            OPTIONAL {{
                                ?song wdt:P136 ?genre ;
                                    wdt:P577 ?releaseDate .
                                ?sameGenreSong wdt:P136 ?genre ;
                                    wdt:P577 ?sameGenreReleaseDate ;
                                    wdt:P175 ?sameGenreArtist ;
                                    wdt:P31/wdt:P279* wd:Q7366 ;
                                    rdfs:label ?recommendedSongLabel .
                                ?sameGenreArtist rdfs:label ?recommendedArtistLabel .
                    
                                FILTER (abs(year(?releaseDate) - year(?sameGenreReleaseDate)) <= 2 )
                                FILTER (lang(?recommendedSongLabel) = "en" && lang(?recommendedArtistLabel) = "en" )
                            }}

                            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
                        }}
                        ORDER BY RAND()
                        LIMIT 5"""

    sparql.setQuery(query_wikidata)

    results_list = []
    try:
        result = sparql.queryAndConvert()

        for row in result["results"]["bindings"]:
            song_label = row["recommendedArtistLabel"]["value"]
            artist_label = row["recommendedSongLabel"]["value"]
            results_list.append((artist_label, song_label))

    except Exception as e:
        print(e)

    return results_list

def clean_label(label):
    
    #Remove any text in parentheses from a string.
    return re.sub(r'\s*\([^)]*\)', '', label)