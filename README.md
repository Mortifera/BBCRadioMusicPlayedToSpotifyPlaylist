## Project Overview
This project is designed to interact with the SimpleScraper API to fetch episode and music data, and then use the Spotify API to search for and add tracks to a Spotify playlist.

## Installation
To run this project, you need to have Python installed on your system. Clone the repository and install the required dependencies by running:

```
pip install -r requirements.txt
```

## Configuration
Before running the scripts, you need to set up the `.env` file with the necessary API keys and endpoints. Here is a template for the `.env` file:

```
SIMPLE_SCRAPER_FIND_MUSIC_PLAYED_BASE_URL=<simple_scraper_find_music_played_endpoint>
SIMPLE_SCRAPER_LIST_EPISODES_BASE_URL=<simple_scraper_list_episodes_endpoint>
SIMPLE_SCRAPER_RUN_NOW=true # Set to false if you want to run the scraper and have it fetch cached results

SPOTIFY_APP_CLIENT_ID=<your_spotify_client_id>
SPOTIFY_APP_CLIENT_SECRET=<your_spotify_client_secret>
SPOTIFY_PLAYLIST_ID=<your_spotify_playlist_id>
```

Replace the values with the appropriate values.

### SimpleScraper Setup

To setup simple scraper first go to: https://simplescraper.io/ and create an account.

Then you can use the following links to create the API endpoints for find music played and list episodes:
* Find Music Played: https://simplescraper.io/?sharedRecipe=OUURg8kASjuxbXvdGO0B
* List Episodes: https://simplescraper.io/?sharedRecipe=lif7as8Izq4szUQ1hCOg

Then on the left sidebar go to "My Recipes" and then click each recipe, then go to the "API" tab and copy the API URL and paste it into the `.env` file (per recipe).

### Spotify Setup

To setup Spotify, first go to: https://developer.spotify.com/dashboard/ and create an account.

Then create a new app and copy the client id and client secret into the `.env` file. Make sure to set the redirect uri to `http://localhost:8080/callback`; the title and description etc do not matter though.

Then go to the Spotify playlist and copy the playlist link. If the link is for example https://open.spotify.com/playlist/0rdglpsZ8cnh9KMUMVcRhS?si=04bacdc94efd477c then the playlist url is 0rdglpsZ8cnh9KMUMVcRhS (the part after playlist/ and before ?si=). Copy this into the `.env` file for the `SPOTIFY_PLAYLIST_ID` variable.

## Usage
To run the main script, execute:

```
python script.py
```

This will process the latest episodes, find music played in those episodes, and add the tracks to the specified Spotify playlist.

## Contributing
Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.