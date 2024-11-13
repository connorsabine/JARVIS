import logging
import datetime

def log_info(text):
    logging.info(datetime.time() + " - " + text)

def log_error(text):
    logging.error(datetime.time() + " - " + text)


def log_request(text, level):
    if text is None:
        text = "No Text"

    if level == "info":
        logging.info(datetime.time() + " - " + "Request: " + text)
    else:
        logging.error(datetime.time() + " - " + "Request: " + text)


def log_response(text, level, type):
    if text is None:
        text = "No Text"

    if level == "info":
        logging.info(datetime.time() + " - " + "Response: " + text + "(" + type + ")")
    else:
        logging.error(datetime.time() + " - " + "Response: " + text + "(" + type + ")")