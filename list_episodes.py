import requests
from typing import Any, List
from dotenv import load_dotenv
import os

from typing import TypedDict

class EpisodeInfo(TypedDict):
    episode: str
    episode_link: str

def fetch_episode_data(api_key: str, run_now: str, base_url: str) -> Any:
    """
    Fetch episode data from the SimpleScraper API using the provided API key and run_now parameter.

    :param api_key: The API key for SimpleScraper.
    :param run_now: The run_now parameter to trigger the scraper immediately.
    :param base_url: The base URL for the SimpleScraper API.
    :return: The JSON response data from the API.
    """
    url = base_url
    params = {
        "apikey": api_key,
        "limit": "1000",
        "run_now": run_now
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    return response.json()

def ListEpisodes() -> List[EpisodeInfo]:
    """
    List all episodes by fetching data from the SimpleScraper API and parsing it into a list of EpisodeInfo.

    :return: A list of EpisodeInfo dictionaries containing episode details.
    """
    # Load environment variables
    load_dotenv()
    SIMPLE_SCRAPER_API_KEY = os.getenv('SIMPLE_SCRAPER_API_KEY')
    SIMPLE_SCRAPER_RUN_NOW = os.getenv('SIMPLE_SCRAPER_RUN_NOW', 'false')
    SIMPLE_SCRAPER_LIST_EPISODES_BASE_URL = os.getenv('SIMPLE_SCRAPER_LIST_EPISODES_BASE_URL')

    data = fetch_episode_data(SIMPLE_SCRAPER_API_KEY, SIMPLE_SCRAPER_RUN_NOW, SIMPLE_SCRAPER_LIST_EPISODES_BASE_URL)
    episodes = [EpisodeInfo(episode=item['episode'], episode_link=item['episode_link']) for item in data.get("data", [])]

    # Filter the episodes to make sure they have unique links
    filtered_episodes: List[EpisodeInfo] = []

    for episode in episodes:
        if episode['episode_link'] not in [item['episode_link'] for item in filtered_episodes]:
            filtered_episodes.append(episode)

    return filtered_episodes

# Example usage:
if __name__ == "__main__":
    episodes = ListEpisodes()
    for episode in episodes:
        print(episode["episode"], episode["episode_link"])
