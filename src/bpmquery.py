import externalquery
from SPARQLWrapper import SPARQLWrapper, JSON

def get_bpm(song, artist):

    results_list = []
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    #for song_title, artist_name:
        # SPARQL query to fetch BPM for a given song and artist
    query = f"""
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?song ?songLabel ?artist ?artistLabel ?bpm WHERE {{
                ?song wdt:P31 wd:Q7366 ;  # Instance of a musical work
                    wdt:P175 ?artist ;  # Performer/artist
                    wdt:P1725 ?bpm .   # BPM property

                ?song rdfs:label ?songLabel .
                ?artist rdfs:label ?artistLabel .

                FILTER(LANG(?songLabel) = "en" && LANG(?artistLabel) = "en")
                
            }}
            LIMIT 100
        """
    sparql.setQuery(query)

    try:
            # Execute the query and process the results
            results = sparql.queryAndConvert()
            for row in results["results"]["bindings"]:
                bpm = float(row["bpm"]["value"])
                category = classify_bpm(bpm)
                results_list.append((
                    row["songLabel"]["value"],
                    row["artistLabel"]["value"],
                    bpm,
                    category
                ))
    except Exception as e:
            print(f"Error fetching BPM for '{song}' by '{artist}': {e}")
    return category
            
# Classify BPM
def classify_bpm(bpm):
    bpm = float(bpm)
    if bpm <= 90:
        return "Low"
    elif 91 <= bpm <= 140:
        return "Medium"
    else:
        return "High"
