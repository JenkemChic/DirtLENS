from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import socket

def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def get_current_position():
    if not is_connected():
        return None, None

    geolocator = Nominatim(user_agent="myGeocoder")

    try:
        location = geolocator.geocode("175 5th Avenue NYC")

        if location is not None:
            return location.latitude, location.longitude
        else:
            raise Exception("Unable to retrieve location")
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        raise Exception(f"Geocoder error: {e}")
