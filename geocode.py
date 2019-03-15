import geocoder
import math


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

# Used by default, when there are no location services available
DEFAULT_LOCATION = SimpleNamespace(**{
    'latitude': '41.55926513671875',
    'longitude': '-8.405625509894655',
    'altitude': 190.0,
    'city': 'Braga',
    'country': 'Portugal',
    'dms_latitude': '41°33\'33.38\" E',
    'dms_longitude': '8°24\'20.5\" S',
})


def dd2dms(longitude, latitude):
    """ Convert decimal-degrees (DD) to degrees-minutes-seconds (DMS).

        Original version by Glen Bambrick (https://glenbambrick.com/2015/06/24/dd-to-dms/)

        Converted to Python 3.7 and adapted by Victor Domingos
    """
    split_degx = math.modf(longitude)
    degrees_x = int(split_degx[1])
    minutes_x = abs(int(math.modf(split_degx[0] * 60)[1]))
    seconds_x = abs(round(math.modf(split_degx[0] * 60)[0] * 60, 2))

    # repeat for latitude
    split_degy = math.modf(latitude)
    degrees_y = int(split_degy[1])
    minutes_y = abs(int(math.modf(split_degy[0] * 60)[1]))
    seconds_y = abs(round(math.modf(split_degy[0] * 60)[0] * 60, 2))

    # account for E/W & N/S
    if degrees_x < 0:
        EorW = "W"
    else:
        EorW = "E"

    if degrees_y < 0:
        NorS = "S"
    else:
        NorS = "N"

    # abs() remove negative from degrees, was only needed for if-else above
    dms_lat = str(abs(degrees_x)) + u"\u00b0" + str(minutes_x) + "'" + str(
        seconds_x) + "\" " + EorW
    dms_lng = str(abs(degrees_y)) + u"\u00b0" + str(minutes_y) + "'" + str(
        seconds_y) + "\" " + NorS
    return dms_lat, dms_lng


def obter_localizacao():
    try:
        console.show_activity()
        location.start_updates()
        coordinates = location.get_location()
        location.stop_updates()
        console.hide_activity()
        results = location.reverse_geocode(coordinates)
        pais = results[0]['CountryCode']
        dms_lat, dms_lng = dd2dms(coordinates['latitude'],
                                  coordinates['longitude'])

        cur_location = {
            'latitude': coordinates['latitude'],
            'longitude': coordinates['longitude'],
            'city': results[0]['City'],
            'country': results[0]['Country'],
            'altitude': float(coordinates['altitude']),
            'dms_latitude': dms_lat,
            'dms_longitude': dms_lng,
        }
        return SimpleNamespace(**cur_location)
    except Exception as e:
        print(e)
        print('Não foi possível obter a localização atual.'
              '\nA utilizar predefinição...\n')
        console.hide_activity()
        return None


def get_current_coordinates():
    g = geocoder.ip('me')
    dms_lat, dms_lng = dd2dms(g.latlng[0], g.latlng[1])
    print(g)
    cur_location = {
        'latitude': g.latlng[0],
        'longitude': g.latlng[1],
        'city': g.city,
        'country': g.country,
        'altitude': None,
        'dms_latitude': dms_lat,
        'dms_longitude': dms_lng,
    }

    return SimpleNamespace(**cur_location)


if __name__ == "__main__":
    device_location = None
    try:
        if IS_IOS:
            device_location = obter_localizacao()
            source = 'network or device data'
        else:
            device_location = get_current_coordinates()
            source = 'current IP address'
    except Exception as e:
        print(e)
        pass
    if device_location is None:
        device_location = DEFAULT_LOCATION
        source = 'application default settings'

    print(
        f'\nBased on the {source}, these are the coordinates for your current location:\n'
    )
    print(
        f'  {device_location.dms_latitude} {device_location.dms_longitude}\n  {device_location.city}, {device_location.country}'
    )
    if device_location.altitude is None:
        print(f'  Altitude: <undetermined>')
    else:
        print(f'  Altitude: {device_location.altitude:.0f}m\n')
