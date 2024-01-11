import os
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, TypedDict
import webbrowser
import requests
from urllib.parse import urlencode
import time
import threading
import uvicorn

from typing import Dict, List, TypedDict

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
CLIENT_ID = os.getenv('SPOTIFY_APP_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_APP_CLIENT_SECRET') 
REDIRECT_URI = "http://localhost:8000/callback"
SCOPE = "user-read-private playlist-modify-private playlist-modify-public"

access_token = None
token_expires = 0

class SpotifyTrackInfo(TypedDict):
    name: str
    artists: List[str]
    album_name: str
    external_urls: Dict[str, str]

def is_track_in_playlist(track_id: str, playlist_id: str) -> bool:
    ensure_access_token()
    headers = get_spotify_headers()
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    params = {"fields": "items(track(id))", "limit": 100}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    tracks_data = response.json().get('items', [])
    for item in tracks_data:
        if item['track']['id'] == track_id:
            return True
    return False

def add_song_to_playlist(track_id: str, playlist_id: str) -> None:
    ensure_access_token()
    headers = get_spotify_headers()
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    data = {"uris": [f"spotify:track:{track_id}"]}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

def get_auth_query() -> str:
    """
    Generate the query string for Spotify authentication.

    :return: The encoded query string for the authentication URL.
    """
    global auth_state
    # generate randomised string
    auth_state = str(uuid.uuid4())
    query = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "state": auth_state
    }
    return urlencode(query)

def get_spotify_headers() -> Dict[str, str]:
    """
    Get the authorization headers for Spotify API requests.

    :return: A dictionary containing the Authorization header.
    """
@app.get("/login")
def login():
    query = get_auth_query()
    return RedirectResponse(f"{SPOTIFY_AUTH_URL}?{query}")

@app.get("/callback")
def callback(code: str, state: str):
    global access_token, token_expires, auth_state
    if state != auth_state:
        raise HTTPException(status_code=400, detail="State mismatch")
    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(SPOTIFY_TOKEN_URL, data=body)
    response.raise_for_status()
    token_info = response.json()
    access_token = token_info['access_token']
    token_expires = time.time() + token_info['expires_in']
    return {"message": "Authentication successful"}

def get_spotify_headers():
    global access_token, token_expires
    if time.time() >= token_expires:
        raise HTTPException(status_code=401, detail="Token expired")
    return {"Authorization": f"Bearer {access_token}"}

def is_token_valid() -> bool:
    """
    Check if the current Spotify access token is valid.

    :return: True if the token is valid, False otherwise.
    """
def is_token_valid() -> bool:
    global access_token, token_expires, last_time_checked
    if access_token is None or time.time() >= token_expires:
        return False

    if "last_time_checked" not in globals():
        last_time_checked = time.time()

    if time.time() - last_time_checked <= 600:
        last_time_checked = time.time()
        return True

    last_time_checked = time.time()

    try:
        headers = get_spotify_headers()
        response = requests.get("https://api.spotify.com/v1/me", headers=headers)
        return response.status_code == 200
    except:
        return False

def ensure_access_token():
    """
    Ensure that a valid Spotify access token is available. If not, start the authentication process.

    Explanation of Authorization Code Flow: https://developer.spotify.com/documentation/web-api/tutorials/code-flow

    To summarise the flow:
    1. Redirect the user to the Spotify authorization page to log in.
    2. After logging in, the user is redirected to the callback URL with a code.
    3. Exchange the code for an access token.
    4. Use the access token to make requests to the Spotify API.

    """
    if is_token_valid():
        return

    global access_token

    def start_server():
        uvicorn.run(app, host="localhost", port=8000)

    # Start the FastAPI server in a new thread
    threading.Thread(target=start_server, daemon=True).start()

    # Give the server a moment to start
    time.sleep(1)

    # Open the browser to the login page
    webbrowser.open("http://localhost:8000/login")

    # Wait for the user to log in
    input("Press Enter to continue...")

    if is_token_valid():
        print("Token is valid.")
    else:
        print("Token is not valid.")
        raise HTTPException(status_code=401, detail="Authentication failed")

def search_song(song_name: str, artist_name: str = "") -> List[SpotifyTrackInfo]:
    """
    Search for a song on Spotify using the song name and optionally the artist name.

    :param song_name: The name of the song to search for.
    :param artist_name: The name of the artist to include in the search.
    :return: A list of SpotifyTrackInfo dictionaries containing the search results.
    """
    ensure_access_token()
    headers = get_spotify_headers()
    query = song_name
    if artist_name:
        query += f" artist:{artist_name}"
    params = {"q": query, "type": "track"}
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    tracks = data['tracks']['items']
    return [
        SpotifyTrackInfo(
            name=track['name'],
            artists=[artist['name'] for artist in track['artists']],
            album_name=track['album']['name'],
            external_urls=track['external_urls']
        ) for track in tracks
    ]
