from SPARQLWrapper import SPARQLWrapper, JSON

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
            song_label = row["artistLabel"]["value"]
            artist_label = row["songLabel"]["value"]
            results_list.append((artist_label, song_label))
            
    except Exception as e:
        print(e)

    return results_list


def wikidata_query(artistName : str, songName : str):
    #connect to the Wikidata SPARQL endpoint
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    # Check https://www.wikidata.org/wiki/Wikidata:Main_Page for finding P31, and Q7366
    query_wikidata = f"""SELECT DISTINCT ?song ?songLabel ?artist ?artistLabel WHERE {{
                        ?song wdt:P31 wd:Q55850593 ;
                                wdt:P175 ?artist ;
                                rdfs:label ?songLabel .
                            ?artist rdfs:label ?artistLabel .
                        FILTER(CONTAINS(?artistLabel, "{artistName}")) .
                        FILTER(LANG(?artistLabel) = "en" && LANG(?songLabel) = "en") .
                        }} LIMIT 5"""
    

    query_wikidata2 = f"""SELECT DISTINCT ?recommendedSong ?recommendedSongLabel WHERE {{
                        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }}

                        ?song rdfs:label "{songName}"@en.
                        ?song wdt:P175 ?artist.
                        ?song wdt:P136 ?genre.
                        ?song wdt:P264 ?musicLabel.
                        ?song wdt:P495 ?country.
                        ?song wdt:P175 ?collaborator.
                        
                        ?artist rdfs:label "{artistName}"@en.
                        ?artist wdt:P941 ?inspiredBy.
                                
                        {{
                            ?recommendedSong wdt:P175 ?collaborator.
                        }} UNION {{
                            ?recommendedSong wdt:P136 ?genre.
                        }} UNION {{
                            ?recommendedSong wdt:P175 ?inspiredBy.
                        }}
                        
                        
                        {{ 
                            ?recommendedSong wdt:P31 wd:Q7366.
                        }} UNION {{
                            ?recommendedSong wdt:P31 wd:Q134556. 
                        }}

                            ?recommendedSong rdfs:label ?recommendedSongLabel.
                            ?recommendedSong wdt:P175 ?recommendedArtist.
                            ?recommendedArtist rdfs:label ?recommendedArtistLabel.

                            FILTER(LANG(?recommendedSongLabel) = "en" && LANG(?recommendedArtistLabel) = "en")

                        }}
                        ORDER BY RAND()
                        LIMIT 5"""

    sparql.setQuery(query_wikidata2)

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