#!/usr/bin/env python3
import geocoder
import math

from constants import DEFAULT_LOCATION

try:
    import sys

    if sys.platform == 'ios':
        import console
        import location

        IS_IOS = True
    else:
        IS_IOS = False
except:
    IS_IOS = False

from types import SimpleNamespace
from typing import Tuple


def dd2dms(latitude: float, longitude: float) -> Tuple[str, str]:
    """ Convert decimal-degrees (DD) to degrees-minutes-seconds (DMS).
        Original version by Glen Bambrick (https://glenbambrick.com/2015/06/24/dd-to-dms/)
        Converted to Python 3.7 and adapted by Victor Domingos
    """

    def _dec_to_dms(dec_number: float) -> Tuple[int, int, float]:
        split_deg = math.modf(dec_number)
        degrees = int(split_deg[1])
        minutes = abs(int(math.modf(split_deg[0] * 60)[1]))
        seconds = abs(round(math.modf(split_deg[0] * 60)[0] * 60, 2))
        return degrees, minutes, seconds

    deg_lat, min_lat, sec_lat = _dec_to_dms(latitude)
    deg_long, min_long, sec_long = _dec_to_dms(longitude)

    if deg_lat < 0:
        NorS = "S"
    else:
        NorS = "N"

    if deg_long < 0:
        EorW = "W"
    else:
        EorW = "E"

    dms_lng = f'{abs(deg_long)}°{min_long}\'{sec_long}"{EorW}'
    dms_lat = f'{abs(deg_lat)}°{min_lat}\'{sec_lat}"{NorS}'
    return dms_lat, dms_lng


def get_location_ios():
    try:
        console.show_activity()
        location.start_updates()
        coordinates = location.get_location()
        location.stop_updates()
        console.hide_activity()
        results = location.reverse_geocode(coordinates)

        if not results:
            results = [{'City': 'N/A', 'Country': 'N/A'}]

        dms_lat, dms_lng = dd2dms(coordinates['latitude'],
                                  coordinates['longitude'])

        return SimpleNamespace(**{
            'latitude': coordinates['latitude'],
            'longitude': coordinates['longitude'],
            'city': results[0]['City'],
            'country': results[0]['Country'],
            'altitude': float(coordinates['altitude']),
            'dms_latitude': dms_lat,
            'dms_longitude': dms_lng,
        })
    except Exception as e:
        print(e.with_traceback)
        print('Não foi possível obter a localização atual.'
              '\nA utilizar predefinição...\n')
        console.hide_activity()
        return None


def get_location_current_ip():
    g = geocoder.ip('me')
    dms_lat, dms_lng = dd2dms(g.latlng[0], g.latlng[1])

    return SimpleNamespace(**{
        'latitude': g.latlng[0],
        'longitude': g.latlng[1],
        'city': g.city,
        'country': g.country,
        'altitude': None,
        'dms_latitude': dms_lat,
        'dms_longitude': dms_lng,
    })


def get_location():
    device_location = None
    try:
        if IS_IOS:
            device_location = get_location_ios()
            source = 'network or device data'
        else:
            device_location = get_location_current_ip()
            source = 'current IP address'
    except Exception as e:
        print(e)
        pass
    if device_location is None:
        device_location = DEFAULT_LOCATION
        source = 'application default settings'
    return device_location, source


if __name__ == "__main__":
    device_location, source = get_location()

    print(
        f'\nBased on the {source}, these are the coordinates for your current location:\n'
    )
    print(
        f'  {device_location.dms_latitude} {device_location.dms_longitude}\n  {device_location.city}, {device_location.country}'
    )
    if device_location.altitude is None:
        print(f'  Alt.: <undetermined>')
    else:
        print(f'  Alt.: {device_location.altitude:.0f}m\n')
