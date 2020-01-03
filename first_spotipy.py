# from github
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

''' show artist genre
    shows the albums and tracks for a given artist.
    select an album and display all tracks
'''

client_id = 'b763b8ddd5084d798ede741a126da272'
client_secret = '476fbb1cb26046fe9514a6f20de534b8'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

# search for artist, print all hits, allow user to select which one
def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']

    for count, artist in enumerate(items):
        print(f" {count + 1}. {items[count]['name']}")

    # get user to select artists
    while True:
        try:
            if len(items) > 0:
                user_choice = int(input("Select artist: "))
                return items[user_choice - 1]
            else:
                return None
        except:
            print('Invalid choice. Try again')


def get_genre(artist):
    genres = ','.join(artist['genres'])
    return genres

# List all albums, user select one of interest
# -- Need to remove duplicates from list
def get_album(artist):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    seen = set()
    albums.sort(key=lambda album:album['name'].lower())
    for album in albums:
        name = album['name']
        if name not in seen:
            seen.add(name)

    for count, album in enumerate(albums):
        print(f"{count + 1}. {album['name']}")

    # get user to select artists
    while True:
        try:
            if len(albums) > 0:
                user_choice = int(input("Select album: "))
                return albums[user_choice - 1]['id']
            else:
                return None
        except:
            print('Invalid choice. Try again')

def show_album_tracks(artist_id):
    tracks = []
    results = sp.album_tracks(album_id)
    tracks.extend(results['items'])

    for track in tracks:
        print(f"{track['track_number']}. {track['name']}")


if __name__ == '__main__':
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    if len(sys.argv) < 2:
        print(f"Script usage: '{sys.argv[0]}' 'artist name'")
    else:
        name = ' '.join(sys.argv[1:])
        artist = get_artist(name)


        print(get_genre(artist))
        album_id = get_album(artist)
        show_album_tracks(album_id)
