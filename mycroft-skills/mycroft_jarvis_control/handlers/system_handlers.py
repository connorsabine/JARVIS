from jarvis import config
from jarvis.features import weather, queryhelper, shutdown, apps, getselfdata

from mycroft import MycroftSkill, intent_file_handler
import logging
import datetime

class SystemControlSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        logging.basicConfig(filename="logs/jarvis.log", level=logging.INFO, format='%(asctime)s - %(message)s')

    @intent_file_handler('whereAmI.intent')
    def handle_where_am_i(self, message):
        location = getselfdata.get_location()
        response = f"You are currently in {location}"
        logging.info(f"Location spoken: {location}")
        return response


    @intent_file_handler('terminalMode.intent')
    def handle_terminal_mode(self, message):
        config.INTERACTION_TYPE = "Terminal"
        response = f"Okay {config.ADDRESS}, switching to terminal mode"
        logging.info("Switched to terminal mode.")
        return response


    @intent_file_handler('voiceMode.intent')
    def handle_voice_mode(self, message):
        config.INTERACTION_TYPE = "Voice"
        response = f"Okay {config.ADDRESS}, switching to voice mode"
        logging.info("Switched to voice mode.")
        return response


    @intent_file_handler('getIP.intent')
    def handle_get_ip(self, message):
        ip = getselfdata.get_ip()
        response = f"Your IP address is {ip}"
        logging.info(f"IP address spoken: {ip}")
        return response


    @intent_file_handler('getWeather.intent')
    def handle_get_weather(self, message):
        response = weather.get_weather(*getselfdata.get_latlng())
        logging.info(f"Weather information spoken: {response}")
        return response


    @intent_file_handler('getTime.intent')
    def handle_get_time(self, message):
        response = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=config.TIME_ZONE))).strftime('%I:%M %p')
        logging.info(f"Time spoken: {response}")
        return response


    @intent_file_handler('getDate.intent')
    def handle_get_date(self, message):
        time = datetime.date.today().strftime('%A, %B %d, %Y')
        response = "Todays date is " + time
        logging.info(f"Date spoken: {time}")
        return response


    @intent_file_handler('shutdown.intent')
    def handle_shutdown(self, message):
        logging.info("Initiating system shutdown.")
        shutdown.power_down()

