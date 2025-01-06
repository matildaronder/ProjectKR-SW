from SPARQLWrapper import SPARQLWrapper, JSON

def dbpedia_query():
    #connect to the DBpedia SPARQL endpoint
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    prefix = """PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX dct: <http://purl.org/dc/terms/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                """

    query_dbpedia = prefix + """SELECT ?song ?songLabel ?artist ?artistLabel WHERE {
                            ?song a dbo:Song ;
                                dbo:artist ?artist .
                            OPTIONAL { ?song rdfs:label ?songLabel FILTER (lang(?songLabel) = "en") }
                            OPTIONAL { ?artist rdfs:label ?artistLabel FILTER (lang(?artistLabel) = "en") }

                        } LIMIT 10"""

    sparql.setQuery(query_dbpedia)

    try:
        result = sparql.queryAndConvert()
        results_list = []

        for row in result["results"]["bindings"]:
            song_label = row["artistLabel"]["value"]
            artist_label = row["songLabel"]["value"]
            results_list.append((song_label, artist_label))
            
    except Exception as e:
        print(e)

    return results_list


def wikidata_query():
    #connect to the Wikidata SPARQL endpoint
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    # Check https://www.wikidata.org/wiki/Wikidata:Main_Page for finding P31, and Q7366
    query_wikidata = """SELECT ?song ?songLabel ?artist ?artistLabel WHERE {
                        ?song wdt:P31 wd:Q7366 ;
                        wdt:P136 wd:Q11399 ;
                        wdt:P175 ?artist .
    
                        SERVICE wikibase:label {
                            bd:serviceParam wikibase:language "en" .
                            }   
                        } LIMIT 10


    """
    sparql.setQuery(query_wikidata)

    try:
        result = sparql.queryAndConvert()

        results_list = []

        for row in result["results"]["bindings"]:
            song_label = row["artistLabel"]["value"]
            artist_label = row["songLabel"]["value"]
            results_list.append((song_label, artist_label))

    except Exception as e:
        print(e)

    return results_list