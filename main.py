from bs4 import BeautifulSoup
import pprint
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

TOP_100_URL = 'https://www.billboard.com/charts/hot-100'
ALL_TITLES = []
ALL_TITLES_URI = []
CLIENT_ID = 'af4ad27d4d86450f9aab76e0551bfbba'
CLIENT_SECRET = '236fbb11a58d463a9efba2bd057c38b7'
USER_ID = '31epb5yfqafml2zbufq6wfotf2vm'
REDIRECT_URI = 'http://example.com'

date = input("Which uear do you want to travel to ? Type the date in this format YYYY-MM-DD:")
year = date.split('-')[0]
response = requests.get(url=f'{TOP_100_URL}/{date}/')
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI,scope='playlist-modify-private'))






soup = BeautifulSoup(response.text, 'html.parser')

all_blocks = soup.findAll(name='div', class_='o-chart-results-list-row-container')
for block in all_blocks:
    title = block.find('h3', id="title-of-a-story").getText().strip()
    ALL_TITLES.append(title)

# Search for song urls
for title in ALL_TITLES:
    result = sp.search(q=f'track:{title} year:{year}', type='track')
    print (result)
    try:
        uri = result['tracks']['items'][0]['uri']
        ALL_TITLES_URI.append(uri)
    except IndexError:
        pass

playlist = sp.user_playlist_create(user=USER_ID, name=f'{date} Billboard 100', public=False)
sp.playlist_add_items(playlist_id=playlist['id'], items=ALL_TITLES_URI)
print(ALL_TITLES)
print(ALL_TITLES_URI)

