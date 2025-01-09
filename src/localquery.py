from rdflib import Graph

def init_graph():
       # Load local turtle file
       g = Graph()
       g.parse("./data/music_data2.ttl", format="turtle")
       return g

def local_query(graph : Graph, time_of_day : str, bpm : str):

    # Define prefix for query, can be used on very query
    prefix = """PREFIX mo: <http://purl.org/ontology/mo/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            """

    # Define specific query for what you looking for, ORDER BY RAND() need to be used for random results everytime.
    query = prefix  + f"""
    SELECT ?SongName ?ArtistName
    WHERE {{
    ?track a mo:Track ;
            mo:performer ?artist ;
            rdfs:label ?SongName ;
            mo:time "{time_of_day}" ;
            mo:ean "{bpm}" .

    ?artist a mo:MusicArtist ;
            rdfs:label ?ArtistName .
    }}
    """

    # SongName, ArtistName defined in query
    results = graph.query(query)
    results_list = []

    for row in results:
       results_list.append((str(row.SongName), str(row.ArtistName)))

    return results_list
