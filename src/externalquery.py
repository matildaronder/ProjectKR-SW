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

def clean_label(label):
    
    #Remove any text in parentheses from a string.
    return re.sub(r'\s*\([^)]*\)', '', label)