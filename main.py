import sys
import spotipy
import spotipy.util as util
import random

scope = 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public'

PLAYLIST_LENGTH_IN_MS = 2 * 60 * 60 * 1000  # 2 hours

USERNAME = ''

token = util.prompt_for_user_token(USERNAME, scope, client_id='', client_secret='', redirect_uri='')

if token:
    sp = spotipy.Spotify(auth=token)
    # results = sp.user_playlists(USERNAME)
    # for item in results['items']:
    #     print(item['name'], item['id'])

    playlist_id = ''

    response = sp.user_playlist(USERNAME, playlist_id=playlist_id)

    print(response['followers'])

    playlist_name = response['name']

    track_list = []

    while len(track_list) == 0 or len(track_list) < total:
        response = sp.user_playlist_tracks(USERNAME, playlist_id, offset=len(track_list))

        track_list += response['items']

        total = response['total']

        if total < 1:
            break

    random.shuffle(track_list)

    playlists = []
    current_playlist_length = 0

    for track in track_list:
        if current_playlist_length == 0:
            current_playlist = []

        current_playlist.append(track)
        current_playlist_length += track['track']['duration_ms']

        if current_playlist_length > PLAYLIST_LENGTH_IN_MS:
            current_playlist_length = 0
            playlists.append(current_playlist)

    name_list = list('California')

    random.shuffle(name_list)

    shuffled_name = ''.join(name_list)

    new_playlist = sp.user_playlist_create(USERNAME, shuffled_name)

    track_ids = []

    for track in track_list:
        if track['track']['id'] is None:
            print(track)
        track_ids.append(track['track']['id'])

    for i in range(0, len(track_ids), 20):
        sp.user_playlist_add_tracks(USERNAME, new_playlist['id'], track_ids[i:i + 20])

    for i, playlist in enumerate(playlists):
        new_playlist = sp.user_playlist_create(USERNAME, shuffled_name + ' Part %d' % i)

        track_ids = []

        for track in playlist:
            track_ids.append(track['track']['id'])

        for i in range(0, len(track_ids), 20):
            sp.user_playlist_add_tracks(USERNAME, new_playlist['id'], track_ids[i:i + 20])


else:
    print("Can't get token for", USERNAME)
