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


def clean_label(label):
    
    #Remove any text in parentheses from a string.
    return re.sub(r'\s*\([^)]*\)', '', label)

def wikidata_query(artistName : str):
    #connect to the Wikidata SPARQL endpoint
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    # Check https://www.wikidata.org/wiki/Wikidata:Main_Page for finding P31, and Q7366
    query_wikidata = f"""SELECT ?song ?songLabel ?artist ?artistLabel WHERE {{
                        ?song wdt:P31 wd:Q7366 ;
                                wdt:P175 ?artist ;
                                rdfs:label ?songLabel .
                            ?artist rdfs:label ?artistLabel .
                        FILTER(CONTAINS(?artistLabel, "{artistName}")) .
                        FILTER(LANG(?artistLabel) = "en" && LANG(?songLabel) = "en") .
                        }} LIMIT 5"""
    sparql.setQuery(query_wikidata)

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


def wikidata_query_nationality_genre(artistName : str):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    wikidata_query = f"""SELECT ?song ?singerName ?nationality 
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
    LIMIT 50"""

    sparql.setQuery(wikidata_query)

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


def wikidata_query_age(artistName : str):

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)
    wikidata_query = f"""SELECT ?otherSinger ?otherSingerName ?birthYear
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
    LIMIT 50"""
    
    sparql.setQuery(wikidata_query)

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
