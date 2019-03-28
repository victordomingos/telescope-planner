from skyfield.api import load

# Skipping Earth, since we are not planning to support observatories from other planets
SOLAR_SYSTEM = ['sun', 'mercury', 'venus', 'moon', 'mars',
                'JUPITER BARYCENTER', 'URANUS BARYCENTER',
                'NEPTUNE BARYCENTER', 'PLUTO BARYCENTER']

ts = load.timescale()
NOW = ts.now()

# Used by default, when there are no location services available
DEFAULT_LOCATION = SimpleNamespace(**{
    'latitude': 41.55926513671875,
    'longitude': -8.405625509894655,
    'altitude': 190.0,
    'city': 'Braga',
    'country': 'Portugal',
    'dms_latitude': '41°33\'33.38\" N',
    'dms_longitude': '8°24\'20.5\" W',
})

# A few alternative locations, for testing purposes:
ALTERNATIVE_LOCATION1 = SimpleNamespace(**{
    'latitude': 51.1739726374,
    'longitude': -1.82237671048,
    'altitude': 92.0,
    'city': 'Stonehenge',
    'country': 'United Kingdom',
    'dms_latitude': '51°10\'26.30" N',
    'dms_longitude': '-1°49\'20.56" W',
})

ALTERNATIVE_LOCATION2 = SimpleNamespace(**{
    'latitude': 28.304474,
    'longitude': -16.509514,
    'altitude': 2390.0,
    'city': 'Izaña, Teide Observatory',
    'country': 'Tenerife, Spain',
    'dms_latitude': '28°18\'00" N',
    'dms_longitude': '16°30\'35" W',
})

ALTERNATIVE_LOCATION3 = SimpleNamespace(**{
    'latitude': -43.9866667,
    'longitude': 170.4650000,
    'altitude': 1027.0,
    'city': 'Mackenzie Basin, Mt. John Observatory',
    'country': 'New Zealand',
    'dms_latitude': '43°59\'12.0"S',
    'dms_longitude': '170°27\'54.0"E',
})
