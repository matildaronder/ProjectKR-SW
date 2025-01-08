import random

def list_of_songs(results, n=25):
    """
    Select n random songs from the results list.
    If the list has fewer than n songs, return the entire list.
    """
    if len(results) < n:
        print("Not enough songs to select from. Returning all available songs.")
        return results
    return random.sample(results, n)



