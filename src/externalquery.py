from SPARQLWrapper import SPARQLWrapper, JSON
import re

def clean_label(label):
    #Remove any text in parentheses from a string.
    label = re.sub(r'\s*\([^)]*\)', '', label)
    label = re.sub(r'\s*-\s*.*', '', label)
    return label.strip()

def dbpedia_query(artistName : str, songName :str):
    #connect to the DBpedia SPARQL endpoint
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    prefix = """PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX dct: <http://purl.org/dc/terms/>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                """

    query_dbpedia_age = prefix + f"""SELECT ?otherSinger ?otherSingerName ?birthYear
                                    WHERE {{
                                        ?targetSinger rdf:type dbo:MusicalArtist ;
                                                rdfs:label "{artistName}"@en ;
                                                dbo:birthDate ?birthDate .
                                        BIND(YEAR(?birthDate) AS ?targetBirthYear) .
                                
                                ?otherSinger rdf:type dbo:MusicalArtist ;
                                            dbo:birthDate ?otherBirthDate ;
                                            rdfs:label ?otherSingerName .
                                BIND(YEAR(?otherBirthDate) AS ?birthYear) .
                                
                                FILTER (?birthYear >= (?targetBirthYear - 5) && ?birthYear <= (?targetBirthYear + 5)) .

                                # Ensure labels are in English
                                FILTER (lang(?otherSingerName) = "en") .
                                
                                # Exclude the target singer from the results
                                FILTER (?targetSinger != ?otherSinger)
                                    }}
                                    ORDER BY RAND()
                                    LIMIT 5"""
    

    query_dbpedia_nat = prefix + f"""SELECT ?song ?singerName ?nationality 
                                    WHERE {{
                                    ?targetArtist rdf:type dbo:MusicalArtist ;
                                                rdfs:label "{artistName}"@en ;
                                                dbo:birthPlace ?nationality .

                                    ?targetSong rdf:type dbo:MusicalWork ;
                                            dbo:artist ?targetArtist ;
                                            dbo:genre ?genre .

                                    {{
                                    ?singer rdf:type dbo:MusicalArtist ;
                                            dbo:birthPlace ?nationality ;
                                            rdfs:label ?singerName .
                                    }}
                                    UNION
                                    {{
                                    ?singer rdf:type dbo:MusicalArtist ;
                                            dbo:genre ?genre ;
                                            rdfs:label ?singerName .
                                    }}

                                    ?song rdf:type dbo:MusicalWork ;
                                        dbo:artist ?singer .

                                    FILTER (lang(?singerName) = "en")
                                    }}
                                    ORDER BY RAND()
                                    LIMIT 5"""
    
    sparql.setQuery(query_dbpedia_nat)

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
    artist = clean_label(artistName)
    song = clean_label(songName)

    # Check https://www.wikidata.org/wiki/Wikidata:Main_Page for finding P31, and Q7366
    query_wikidata = f""" SELECT DISTINCT ?recommendedSongLabel ?recommendedArtistLabel
                        WHERE {{
                             ?artist rdfs:label "{artist}"@en .

                             {{
                              ?song rdfs:label "{song}"@en ;
                                wdt:P175 ?artist .
                                ?song wdt:P136 ?genre ;
                                    wdt:P577 ?releaseDate .
                                ?sameGenreSong wdt:P136 ?genre ;
                                    wdt:P577 ?sameGenreReleaseDate ;
                                    wdt:P175 ?sameGenreArtist ;
                                    wdt:P31/wdt:P279? wd:Q7366 ;
                                    rdfs:label ?recommendedSongLabel ;
                                    wdt:P407 ?language .
                                ?sameGenreArtist rdfs:label ?recommendedArtistLabel .
                    
                                FILTER (abs(year(?releaseDate) - year(?sameGenreReleaseDate)) <= 2 )
                                FILTER (lang(?recommendedSongLabel) = "en" && lang(?recommendedArtistLabel) = "en" )
                                FILTER (?language IN (wd:Q1860, wd:Q9027))
                            }}
                            UNION 
                            {{
                                ?otherSong wdt:P175 ?artist ;
                                           rdfs:label ?recommendedSongLabel ;
                                           wdt:P31/wdt:P279? wd:Q7366 .
                                ?artist rdfs:label ?recommendedArtistLabel
                                FILTER(?recommendedSongLabel != "{song}" && lang(?recommendedSongLabel) = "en" && lang(?recommendedArtistLabel) = "en")
                            }}

                            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
                        }}
                        ORDER BY RAND()
                        LIMIT 10"""

    sparql.setQuery(query_wikidata)

    results_list = []
    try:
        result = sparql.queryAndConvert()

        for row in result["results"]["bindings"]:
            song_label = row["recommendedArtistLabel"]["value"]
            artist_label = row["recommendedSongLabel"]["value"]
            results_list.append((artist_label, song_label))

    except Exception as e:
        print("Song bad format")
        print(e)

    return results_list