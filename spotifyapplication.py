import json
import sys
from pprint import pprint
import time
from datetime import date
from time import strftime
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

spotify_get_recently_played_url = 'https://api.spotify.com/v1/me/player/recently-played'
spotify_get_currently_played_url = 'https://api.spotify.com/v1/me/player/currently-playing'


# activate virtual env--> python -m venv spotifyApp and then dir and then spotifyApp\Scripts\activate.bat-->venv created

def create_playlist():
    scope = 'playlist-modify-public'
    username = input('Please enter your username: ')

    token = SpotifyOAuth(scope=scope, username=username)
    spotifyObject = spotipy.Spotify(auth_manager=token)

    playlist_name = input("Enter a playlist name: ")
    playlist_description = input("Enter a playlist description: ")

    spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True,
                                       description=playlist_description)

    user_input = ''
    user_input = input("Enter song name: ")
    list_of_songs = []

    while user_input != '':
        result = spotifyObject.search(q=user_input)
        print(result['tracks']['items'][0]['uri'])
        new_results = result['tracks']['items'][0]['uri']
        list_of_songs.append(new_results)

        pre_playlist = spotifyObject.user_playlists(user=username)
        playlist = pre_playlist['items'][0]['id']
        user_input = input("Enter song name: ")
    spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=list_of_songs)
    print("Playlist successfully created with added songs.")


def get_recent_track(access_token_recent_track):
    response = requests.get(
        spotify_get_recently_played_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token_recent_track}"
        }
    )
    json_resp = response.json()

    tracks = [(tracks["track"]["name"], tracks["track"]["id"], tracks["track"]["artists"]) for
              tracks in json_resp["items"]]

    return tracks


def get_current_playing_track(access_token_current_track):
    response = requests.get(
        spotify_get_currently_played_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token_current_track}"
        }
    )
    json_resp = response.json()

    track_id = json_resp["item"]["id"]
    track_name = json_resp["item"]["name"]
    artists = [artist for artist in json_resp["item"]["artists"]]
    link = json_resp["item"]["external_urls"]["spotify"]

    artist_names = ', '.join([artist["name"] for artist in artists])

    current_track_info = {
        "id": track_id,
        "track_name": track_name,
        "artists": artist_names,
        "link": link
    }

    return current_track_info


def main():
    print("This is a spotify program that can grab recent and current played tracks for the user as well as "
          "create a new playlist and lets the user\nadd songs of their choice to their newly created playlist.")
    print("****************************************************************************************************")
    print("Please enter one of the following options...")
    print("****************************************************************************************************")
    print("If you would like to see some track stats, enter the number (1).")
    print("****************************************************************************************************")
    print("If you would like to create a playlist and add songs to it, enter the number (2).")
    print("****************************************************************************************************")
    print("If you would like to exit the program, enter the number (3).")
    print("****************************************************************************************************")
    user_input = int(input("Please enter a number from the options above: "))
    var = True
    while var == True:
        if user_input == 1:
            print(
                "Please make sure your authentication tokens from 'https://developer.spotify.com/console/get-recently-played/?limit=10&after=1484811043508&before=' "
                " \n or 'https://developer.spotify.com/console/get-users-currently-playing-track/?market=ES&additional_types=' is valid and entered above in the \n "
                "program into their respective variables. ")
            print("********************************************************************************************")
            print("If you would like to view recently played tracks, please enter the number (1).")
            print("********************************************************************************************")
            print("If you would like to view currently playing track, please enter the number (2).")
            print("********************************************************************************************")
            print("If you would like to exit the program, enter the number (3).")
            print("********************************************************************************************")
            input_stats = int(
                input("Please enter a number from the options above: "))
            if input_stats == 1:
                ACCESS_TOKEN_RECENT_TRACK = input("Please enter the recent track token from the link pasted above: ")
                recent_track_info = get_recent_track(ACCESS_TOKEN_RECENT_TRACK)
                pprint(
                    recent_track_info,
                    indent=4,
                )

            elif input_stats == 2:
                ACCESS_TOKEN_CURRENT_TRACK = input("Please enter the current track token from the link pasted above: ")
                current_track_info = get_current_playing_track(ACCESS_TOKEN_CURRENT_TRACK)
                pprint(
                    current_track_info,
                    indent=4,
                )
                current_track_id = None
                while True:
                    current_track_info = get_current_playing_track(ACCESS_TOKEN_CURRENT_TRACK)

                    if current_track_info['id'] != current_track_id:
                        pprint(
                            current_track_info,
                            indent=4,
                        )
                        current_track_id = current_track_info['id']

                    time.sleep(1)

            elif input_stats == 3:
                print("You have successfully exited the program.")
                var = False
            else:
                sys.exit("Invalid entry!")


        elif user_input == 2:
            create_playlist()
            exit(0)

        elif user_input == 3:
            print("You have successfully exited the program.")
            var = False

        else:
            sys.exit("Invalid entry!")


if __name__ == '__main__':
    main()
