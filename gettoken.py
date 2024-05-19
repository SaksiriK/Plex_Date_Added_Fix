import requests
import base64
from config import PLEX_USERNAME, PLEX_PASSWORD

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

# Example usage
token = getToken()
if token:
    print("Authentication token:", token)
