from datetime import datetime
import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy import SpotifyOAuth

# Constant datatypes
BILLBOARD_ENDPOINT = "https://www.billboard.com/charts/hot-100/"
year = int(input("enter the year :"))
month = int(input("enter the month :"))
day = int(input("enter the day of the month  :"))
music_date = datetime(year, month, day).strftime("%Y-%m-%d")
url = f'{BILLBOARD_ENDPOINT}{music_date}/'
SCOPE = "playlist-modify-private"
CLIENT_ID = "your client id"
CLIENT_SECRET = "Your client sceret"
redirect_uri = "http://example.com"

# web scraping
website_html = requests.get(url).text
soup = BeautifulSoup(website_html, "html.parser")
content = soup.select(selector="main ul li h3")
list_of_songs = [i.text.strip() for i in content]

# searching the songs
song_uri = []
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=SCOPE,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=redirect_uri,
        show_dialog=True,
        cache_path="token.txt"
    )
)
for song in list_of_songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uri.append(uri)
    except IndexError:
        # print(f"{song} doesn't exist in spotify , Skipped.")
        pass
user_id = sp.current_user()['id']
playlist = sp.user_playlist_create(user=user_id, name=f"{music_date} BillBoard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uri)
