import requests
import base64
from datetime import datetime, timedelta
from config import PLEX_USERNAME, PLEX_PASSWORD
from plexapi.server import PlexServer


def getToken():
    myUrl = 'https://plex.tv/users/sign_in.json'
    base64string = base64.b64encode(f'{PLEX_USERNAME}:{PLEX_PASSWORD}'.encode()).decode()

    headers = {
        'X-Plex-Product': 'YourPlexApp',
        'X-Plex-Client-Identifier': 'YourAppIdentifier',
        'X-Plex-Version': '1.0',
        'Authorization': f'Basic {base64string}'
    }

    dummy_data = {'Barkley': 'IsAFineDog'}

    response = requests.post(myUrl, headers=headers, data=dummy_data)

    if response.status_code == 200 or response.status_code == 201:
        jsonResponse = response.json()
        return jsonResponse['user']['authentication_token']
    else:
        print(f"Failed to get token. Status code: {response.status_code}")
        print("Response content:", response.text)  # Print response content
        return None


# Get authentication token
token = getToken()
if not token:
    exit("Failed to get authentication token.")

# Set up Plex server connection
baseurl = 'http://192.168.1.52:32400' # Your Plex IP address and port
plex = PlexServer(baseurl, token)


def main():
    # Ask for the movie name
    movie_name = input("Enter the name of the movie to search: ")
    print(f"Searching for movie: {movie_name}")

    # Search for the movie
    movie_search_results = plex.search(movie_name)
    if not movie_search_results:
        print("No movie found with that name.")
        return

    # Get the first search result (assuming there's only one)
    movie = movie_search_results[0]

    # Print current metadata related to dates
    print("\nMetadata related to dates:")
    print(f"Added At: {movie.addedAt}")
    print(f"Last Rated At: {movie.lastRatedAt}")
    print(f"Last Viewed At: {movie.lastViewedAt}")
    print(f"Updated At: {movie.updatedAt}")
    print(f"Originally Available At: {movie.originallyAvailableAt}")

    # Update date fields to be today less one week (last week)
    today = datetime.today().date()
    last_week = today - timedelta(weeks=1)

    # Check and update Added At
    if movie.addedAt.date() > last_week:
        print("\nUpdating Added At...")
        setattr(movie, 'addedAt', last_week)
        print("Added At updated successfully!")

    # Check and update Last Viewed At
    if movie.lastViewedAt and movie.lastViewedAt.date() > last_week:
        print("\nUpdating Last Viewed At...")
        setattr(movie, 'lastViewedAt', last_week)
        print("Last Viewed At updated successfully!")

    # Check and update Updated At
    if movie.updatedAt.date() > last_week:
        print("\nUpdating Updated At...")
        setattr(movie, 'updatedAt', last_week)
        print("Updated At updated successfully!")

    # Check and update Originally Available At
    if movie.originallyAvailableAt.date() > last_week:
        print("\nUpdating Originally Available At...")
        setattr(movie, 'originallyAvailableAt', last_week)
        print("Originally Available At updated successfully!")

    # Reread the record and print the date fields again
    print("\nUpdated metadata:")
    movie.reload()
    print(f"Added At: {movie.addedAt}")
    print(f"Last Rated At: {movie.lastRatedAt}")
    print(f"Last Viewed At: {movie.lastViewedAt}")
    print(f"Updated At: {movie.updatedAt}")
    print(f"Originally Available At: {movie.originallyAvailableAt}")


if __name__ == "__main__":
    main()
