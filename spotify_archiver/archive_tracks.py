import spotipy
import spotipy.util as util
from spotify_config import USERNAME, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, RELEASE_RADAR_ARCHIVE_ID, DISCOVER_WEEKLY_ARCHIVE_ID

SCOPE = "playlist-read-private playlist-modify-private"

def get_track_ids(playlist_id):
    tracks = spotify.user_playlist(USERNAME, playlist_id, fields="tracks.items(track(name,id))")['tracks']['items']
    return set(map(lambda x: x['track']['id'], tracks))

token = util.prompt_for_user_token(USERNAME, SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
if token:
    spotify = spotipy.Spotify(auth=token)
    playlists = spotify.current_user_playlists()['items']

    release_radar_id = list(filter(lambda x: (x['name'] == "Release Radar"), playlists)).pop()['id']
    discover_weekly_id = list(filter(lambda x: (x['name'] == "Discover Weekly"), playlists)).pop()['id']

    release_radar_archive_track_ids = get_track_ids(RELEASE_RADAR_ARCHIVE_ID)
    discover_weekly_archive_track_ids = get_track_ids(DISCOVER_WEEKLY_ARCHIVE_ID)

    # do not add songs that already exist in the archive
    release_radar_track_ids = get_track_ids(release_radar_id).difference(release_radar_archive_track_ids)
    discover_weekly_track_ids = get_track_ids(discover_weekly_id).difference(discover_weekly_archive_track_ids)

    if release_radar_track_ids:
        spotify.user_playlist_add_tracks(USERNAME, RELEASE_RADAR_ARCHIVE_ID, release_radar_track_ids, position=0)
    if discover_weekly_track_ids:
        spotify.user_playlist_add_tracks(USERNAME, DISCOVER_WEEKLY_ARCHIVE_ID, discover_weekly_track_ids, position=0)

else:
    print("Token retrieval failed.")
