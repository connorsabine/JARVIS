import spotipy
from spotipy.oauth2 import SpotifyOAuth
from jarvis import config

SPOTIPY_REDIRECT_URI = 'http://google.com/callback/'
scope = "user-read-playback-state,user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.SPOTIPY_CLIENT_ID,
                                               client_secret=config.SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

def play_song(song_name):
    try:
        results = sp.search(q=song_name, limit=1, type='track')
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_uri = track['uri']
            sp.start_playback(uris=[track_uri])
            return f"Playing {track['name']} by {track['artists'][0]['name']}"
        else:
            return "Song not found"
        
    except Exception as e:
        return f"There was an error playing {song_name}"
    

def get_playlists():
    try:
        playlists = sp.current_user_playlists()
        return [playlist['name'] for playlist in playlists['items']]
    except Exception as e:
        return "Error getting playlists"


def play_playlist(playlist_name):
    try:
        playlists = sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'].lower() == playlist_name.lower():
                playlist_uri = playlist['uri']
                sp.start_playback(context_uri=playlist_uri)
                return f"Playing {playlist_name}"
        return "Playlist not found"
    except Exception as e:
        return f"There was an error playing {playlist_name}"

def pause():
    try:
        sp.pause_playback()
        return "Pausing playback"
    except Exception as e:
        return "Error pausing playback"

def resume():
    try:
        sp.start_playback()
        return "Resuming playback"
    except Exception as e:
        return "Error resuming playback"

def next_song():
    try:
        sp.next_track()
        return "Playing next song"
    except Exception as e:
        return "Error playing next song"
    

def previous_song():
    try:
        sp.previous_track()
        return "Playing previous song"
    except Exception as e:
        return "Error playing previous song"

def get_current_song():
    try:
        current_song = sp.current_playback()
        if current_song['item']:
            song = current_song['item']
            return f"Currently playing {song['name']} by {song['artists'][0]['name']}"
        else:
            return "No song currently playing"
    except Exception as e:
        return "Error getting current song"
    
def get_current_playlist():
    try:
        current_playlist = sp.current_playback()
        if current_playlist['context']:
            playlist = sp.playlist(current_playlist['context']['uri'])
            return f"Currently playing {playlist['name']}"
        else:
            return "No playlist currently playing"
    except Exception as e:
        return "Error getting current playlist"

def get_current_volume():
    try:
        current_volume = sp.current_playback()
        if current_volume['device']:
            volume = current_volume['device']['volume_percent']
            return f"Current volume is {volume}%"
        else:
            return "No device currently playing"
    except Exception as e:
        return "Error getting current volume"
    
def set_volume(volume):
    try:
        sp.volume(volume)
        return f"Volume set to {volume}%"
    except Exception as e:
        return f"Error setting volume to {volume}%"

def shuffle():
    try:
        sp.shuffle(True)
        return "Shuffling songs"
    except Exception as e:
        return "Error shuffling songs"