from rdflib import Graph

# Load local turtle file
g = Graph()
g.parse("music_data.ttl", format="turtle")


# Define prefix for query, can be used on very query
prefix = """PREFIX ns1: <http://purl.org/ontology/mo/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            """

# Define specific query for what you looking for, ORDER BY RAND() need to be used for random results everytime.
query = prefix  + """
SELECT ?SongName ?ArtistName
WHERE {
  ?track a ns1:Track ;
         ns1:performer ?artist ;
         rdfs:label ?SongName ;
         ns1:time "Morning" .

  ?artist a ns1:MusicArtist ;
         rdfs:label ?ArtistName .
}
ORDER BY RAND()
LIMIT 10"""

# SongName, ArtistName defined in query
results = g.query(query)
for row in results:
    print(f" Name: {row.SongName} , Arist: {row.ArtistName}")