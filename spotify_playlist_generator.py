import os
import sys
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from difflib import SequenceMatcher

# Spotify API credentials - set these as environment variables
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI', 'http://localhost:8888/callback')
SCOPE = 'playlist-modify-public playlist-modify-private'


def similar(a: str, b: str) -> float:
    """Return similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def get_or_create_playlist(sp: Spotify, user_id: str, name: str) -> str:
    """Get existing playlist ID by name or create a new one."""
    playlists = sp.current_user_playlists(limit=50)
    while playlists:
        for pl in playlists['items']:
            if pl['name'].lower() == name.lower():
                print(f"Found existing playlist: {name}")
                return pl['id']
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            break
    # Not found - create new
    new_pl = sp.user_playlist_create(user_id, name)
    print(f"Created new playlist: {name}")
    return new_pl['id']


def load_bands(file_path: str) -> list:
    """Read band names from a local text file, one per line."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)


def main():
    # Authenticate
    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ))

    user = sp.current_user()
    user_id = user['id']

    # Ask for playlist name
    playlist_name = input("Enter playlist name: ").strip()
    if not playlist_name:
        print("Playlist name cannot be empty.")
        sys.exit(1)

    # Get or create playlist
    playlist_id = get_or_create_playlist(sp, user_id, playlist_name)

    # Load band names
    file_path = input("Enter path to band names file: ").strip()
    bands = load_bands(file_path)

    # For each band, search and add top 4 distinct songs
    for band in bands:
        print(f"Processing band: {band}")
        results = sp.search(q=f"artist:{band}", type='track', limit=20)
        tracks = results['tracks']['items']
        selected = []
        for track in tracks:
            name = track['name']
            # Check similarity against already selected names
            if any(similar(name, sel) > 0.7 for sel in selected):
                continue
            selected.append(name)
            if len(selected) == 4:
                break
        # Map names back to URIs
        uris = [t['uri'] for t in tracks if t['name'] in selected]
        if uris:
            sp.playlist_add_items(playlist_id, uris)
            print(f"Added {len(uris)} tracks for band {band}")
        else:
            print(f"No tracks found for {band}")

    print("Done!")

if __name__ == '__main__':
    main()
