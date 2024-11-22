from jarvis import interface, config
from jarvis.features import audio

from mycroft import MycroftSkill, intent_file_handler
import logging
import subprocess

class SpotifyControlSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        logging.basicConfig(filename="logs/jarvis.log", level=logging.INFO, format='%(asctime)s - %(message)s')


    @intent_file_handler('playSong.intent')
    def handle_play_song(self, message):
        try:
            song = message.split("play ")[1]
            response = audio.play_song(song)
            logging.info(response)
            return response

        except Exception as e:
            response = "Sorry, I couldn't play that song."
            logging.warning("Error playing song.")
            return response


    @intent_file_handler('pauseSpotify.intent')
    def handle_pause(self, message):
        response = audio.pause()
        logging.info(response)
        return response


    @intent_file_handler('unpauseSpotify.intent')
    def handle_unpause(self, message):
        response = audio.resume()
        logging.info(response)
        return response


    @intent_file_handler('getVolumeSpotify.intent')
    def handle_get_volume(self, message):
        response = audio.get_current_volume()
        logging.info(response)
        return response


    @intent_file_handler('setVolumeSpotify.intent')
    def handle_set_volume(self, message):
        try:
            volume = int(''.join(filter(str.isdigit, message.split("set volume ")[1])))
            response = audio.set_volume(volume)
            logging.info(response)
            return response

        except Exception as e:
            response = "Sorry, I couldn't set the volume."
            logging.warning("Error setting volume.")
            return response


    @intent_file_handler('skipSongSpotify.intent')
    def handle_skip_song(self, message):
        response = audio.next_song()
        logging.info(response)
        return response
        
    
    @intent_file_handler('previousSongSpotify.intent')
    def handle_previous_song(self, message):
        response = audio.previous_song()
        logging.info(response)
        return response


    @intent_file_handler('currentSongSpotify.intent')
    def handle_current_song(self, message):
        response = audio.get_current_song()
        logging.info(response)
        return response


    @intent_file_handler('currentPlaylistSpotify.intent')
    def handle_current_playlist(self, message):
        response = audio.get_current_playlist()
        logging.info(response)
        return response


    @intent_file_handler('openSpotify.intent')
    def handle_open_spotify(self, message):
        subprocess.Popen("spotify.exe")
        response = "Opening Spotify"
        logging.info(response)
        return response
