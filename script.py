from dotenv import load_dotenv
from list_episodes import ListEpisodes, EpisodeInfo
from find_music_played import FindMusicPlayed
from spotify_api import search_song, is_track_in_playlist, add_song_to_playlist
from typing import List
import os

def main():
    """
    Main execution function that processes episodes, finds music played, and interacts with Spotify.
    """
    # Load environment variables
    load_dotenv()
    SPOTIFY_PLAYLIST_ID = os.getenv('SPOTIFY_PLAYLIST_ID')
    episodes: List[EpisodeInfo] = ListEpisodes()

    # Filter the episodes to make sure they have unique links
    filtered_episodes: List[EpisodeInfo] = []

    for episode in episodes:
        if episode['episode_link'] not in [item['episode_link'] for item in filtered_episodes]:
            filtered_episodes.append(episode)

    for episode in filtered_episodes:
        print(f"Episode: {episode['episode']}")
        print(f"Link: {episode['episode_link']}")
        music_tracks = FindMusicPlayed(episode['episode_link'])
        for track in music_tracks:
            print(f" - {track.get('artist')} - {track['song']}")
            spotify_tracks = search_song(track['song'], track.get('artist', ''))
            if spotify_tracks:
                spotify_id = spotify_tracks[0]['external_urls']['spotify'].split('/')[-1]
                print(f"Spotify ID: {spotify_id}")
                # Check if the track is already in the playlist
                if not is_track_in_playlist(spotify_id, SPOTIFY_PLAYLIST_ID):
                    # Add the track to the playlist if it's not there
                    add_song_to_playlist(spotify_id, SPOTIFY_PLAYLIST_ID)
                    print(f"Added to playlist: {SPOTIFY_PLAYLIST_ID}")
        print("\n")

# Execute the script
if __name__ == "__main__":
    main()
