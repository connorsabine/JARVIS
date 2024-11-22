import geocoder

def get_ip():
    return geocoder.ip('me').ip

def get_current_city():
    return geocoder.ip('me').city

def get_current_state():
    return geocoder.ip('me').state

def get_current_country():
    return geocoder.ip('me').country

def get_latlng():
    return geocoder.ip('me').latlng

def get_location():
    city = get_current_city()
    state = get_current_state()
    country = get_current_country()
    return f"{city}, {state}, {country}"