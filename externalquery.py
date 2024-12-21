from SPARQLWrapper import SPARQLWrapper, JSON


#connect to the DBpedia SPARQL endpoint
#sparql = SPARQLWrapper("https://dbpedia.org/sparql")
#sparql.setReturnFormat(JSON)
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setReturnFormat(JSON)


prefix = """PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX dct: <http://purl.org/dc/terms/>
            """

query_dbpedia = prefix + """SELECT ?song ?artist WHERE {
                        ?song a dbo:Song ;
                            dbo:artist ?artist .
                    } LIMIT 10"""


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

    for row in result["results"]["bindings"]:
        print(row)
        
except Exception as e:
    print(e)