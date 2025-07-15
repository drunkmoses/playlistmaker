# Spotify Playlist Generator

A Python script that connects to the Spotify Web API to create or update a playlist based on a local list of band names. For each artist, it searches Spotify and adds the top 4 most popular tracks ensuring no two track names are overly similar.

---

## Features

* **Get or Create Playlist**: Prompts for a playlist name and reuses an existing one if it already exists.
* **Bulk Artist Input**: Reads band names from a local text file (one per line).
* **Top Tracks**: Searches Spotify for each band and selects the top 4 most popular tracks.
* **Similarity Filter**: Ensures selected track titles are distinct, skipping overly similar names.

## Prerequisites

* **Python**: Version 3.6 or higher
* **Spotipy**: Spotify Python client library
* **Spotify Developer Account**: You need to register an app to obtain API credentials

### Environment Variables

Set these in your shell or CI environment before running the script:

```bash
export SPOTIPY_CLIENT_ID="your_client_id"
export SPOTIPY_CLIENT_SECRET="your_client_secret"
export SPOTIPY_REDIRECT_URI="http://localhost:8888/callback"
```

## Installation

1. **Clone the repository**

   ```bash
   ```

git clone [https://github.com/yourusername/spotify-playlist-generator.git](https://github.com/yourusername/spotify-playlist-generator.git)
cd spotify-playlist-generator

````

2. **Create a virtual environment** (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate
````

3. **Install dependencies**

   ```bash
   ```

pip install spotipy

````

## Usage

1. **Prepare your band list**: Create a plain text file (e.g., `bands.txt`) with one band or artist name per line.

2. **Run the script**

```bash
python spotify_playlist_generator.py
````

3. **Follow prompts**:

   * Enter the playlist name (existing playlists will be updated, new ones created).
   * Enter the path to your band list file (e.g., `bands.txt`).

Once complete, your Spotify account will have the playlist populated with the top 4 distinct tracks for each band.

## Configuration

* **Similarity Threshold**: The script uses a 0.7 cutoff in `difflib.SequenceMatcher` to filter out similar names. You can adjust this value in the `similar()` function if desired.
* **Search Limit**: By default, it fetches 20 tracks per artist to find distinct titles. You can increase or decrease this in the `sp.search()` call.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
