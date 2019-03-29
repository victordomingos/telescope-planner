#!/usr/bin/env python3
"""
A simple utility for telescope time planning, for astronomy hobbyists. The aim
is to provide an easy to use tool to help planning sky observation sessions,
suggesting some of the interesting objects you may be able to watch at naked
eye, or using amateur equipment (binoculars or small to medium size telescopes)
in a given date/time and place.

© 2019 Victor Domingos (MIT License)
"""
from skyfield.api import load
from pytz import timezone

from telescope_planner.constants import DEFAULT_LOCATION
from telescope_planner.geocode import get_location
from telescope_planner.session import Session


def main():
    print("Welcome to Telescope Planner!")  # DEBUG
    # location, source = get_location()
    location, source = DEFAULT_LOCATION, "DEBUG method"
    ts = load.timescale()
    # now = ts.utc(2019, 3, 29, 1, 39)
    now = ts.now()
    tz = timezone('Europe/Lisbon')

    print(f'\nBased on the {source}, this is your current location:\n')
    print(f'  {location.dms_latitude} {location.dms_longitude}')
    print(f'  {location.city}, {location.country}')
    if location.altitude is None:
        print(f'  Alt.: <undetermined>')
    else:
        print(f'  Alt.: {location.altitude:.0f}m\n')

    session = Session(start=now,
                      end=now,
                      latitude=location.latitude,
                      longitude=location.longitude,
                      altitude=location.altitude,
                      min_alt=0.0,
                      max_alt=90,
                      min_az=None,
                      max_az=None,
                      constellation=None,
                      min_apparent_mag=None,
                      using_catalogs=None)

    # session.log_visible() # DEBUG
    print('\nSolar system:')
    for obj in session.objects_visible.planets:
        obj.update_altaz()
        # print(obj.name, obj.alt, obj.az, obj.distance)
        print(f'{obj.name.ljust(7)} {obj.alt.degrees:8.4f} {obj.az.degrees:7.4f}, {obj.distance.au:5.1f}au')


    print('\nDeep space objects:')
    for obj in session.objects_visible.deepspace:
        obj.update_altaz()
        #print(obj.name, obj.alt, obj.az, obj.distance)
        print(f'{obj.name.ljust(7)} {obj.alt.degrees:8.4f} {obj.az.degrees:7.4f}, {obj.distance.au:5.1f}au')


if __name__ == "__main__":
    main()
