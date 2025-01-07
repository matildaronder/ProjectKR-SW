import random
from externalquery import dbpedia_query, wikidata_query

def list_of_songs(results, n=25):
    """
    Select n random songs from the results list.
    If the list has fewer than n songs, return the entire list.
    """
    if len(results) < n:
        print("Not enough songs to select from. Returning all available songs.")
        return results
    return random.sample(results, n)


    # Example usage:
    if __name__ == "__main__":
        dbpedia_results = dbpedia_query()
        wikidata_results = wikidata_query()

    # Combine the results
    combined_results = dbpedia_results + wikidata_results

    # Select 25 random songs
    random_songs = list_of_songs(combined_results, 25)

    print("\n25 Random Songs:")
    for song, artist in random_songs:
        print(f"Song: {song}, Artist: {artist}")

