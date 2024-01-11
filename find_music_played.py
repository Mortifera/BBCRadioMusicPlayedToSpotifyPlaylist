import requests
from typing import Any, List, TypedDict
from dotenv import load_dotenv
import os

class MusicTrackInfo(TypedDict):
    artist: str
    song: str
    timestamp: int
    timestampString: str
    uid: str
    url: str

def fetch_music_data(api_key: str, source_url: str, run_now: str, base_url: str) -> Any:
    """
    Fetch music data from the SimpleScraper API using the provided API key, source URL, and run_now parameter.

    :param api_key: The API key for SimpleScraper.
    :param source_url: The source URL to scrape.
    :param run_now: The run_now parameter to trigger the scraper immediately.
    :param base_url: The base URL for the SimpleScraper API.
    :return: The JSON response data from the API.
    """
    url = base_url
    params = {"apikey": api_key, "source_url": source_url, "run_now": run_now, "limit": "1000"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def FindMusicPlayed(source_url: str) -> List[MusicTrackInfo]:
    """
    Find music played by fetching data from the SimpleScraper API and parsing it into a list of MusicTrackInfo.

    :param source_url: The source URL to scrape for music tracks.
    :return: A list of MusicTrackInfo dictionaries containing music track details.
    """
    # Load environment variables
    load_dotenv()
    SIMPLE_SCRAPER_API_KEY = os.getenv('SIMPLE_SCRAPER_API_KEY')
    SIMPLE_SCRAPER_RUN_NOW = os.getenv('SIMPLE_SCRAPER_RUN_NOW', 'false')
    SIMPLE_SCRAPER_FIND_MUSIC_PLAYED_BASE_URL = os.getenv('SIMPLE_SCRAPER_FIND_MUSIC_PLAYED_BASE_URL')

    data = fetch_music_data(SIMPLE_SCRAPER_API_KEY, source_url, SIMPLE_SCRAPER_RUN_NOW, SIMPLE_SCRAPER_FIND_MUSIC_PLAYED_BASE_URL)
    return [
        MusicTrackInfo(
            artist=item['artist'],
            song=item['song'],
            timestamp=item['timestamp'],
            timestampString=item['timestampString'],
            uid=item['uid'],
            url=item['url']
        ) for item in data.get("data", [])]
