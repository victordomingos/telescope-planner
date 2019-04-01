#!/usr/bin/env python3
"""
A simple utility for telescope time planning, for astronomy hobbyists. The aim
is to provide an easy to use tool to help planning sky observation sessions,
suggesting some of the interesting objects you may be able to watch at naked
eye, or using amateur equipment (binoculars or small to medium size telescopes)
in a given date/time and place.

© 2019 Victor Domingos (MIT License)
"""
from types import SimpleNamespace

from skyfield.api import Loader
from pytz import timezone

from telescope_planner.constants import DEFAULT_LOCATION, OUR_TOP_LIST_PLANETS, OUR_TOP_LIST_DEEPSPACE
from telescope_planner.settings import DATA_FOLDER
from telescope_planner.geocode import get_location
from telescope_planner.session import Session


def main():
    s = " Welcome to Telescope Planner! "
    line = len(s) * '='
    s = '\n' + line + '\n' + s + '\n' + line
    print(s)  # DEBUG
    # location, source = get_location()
    location, source = DEFAULT_LOCATION, "DEBUG method"
    load = Loader(DATA_FOLDER)
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

    # TODO: The sources variable can be initialized with a list of Messier IDs, for instance
    sources = SimpleNamespace(**{'planets': OUR_TOP_LIST_PLANETS, 'deepspace': OUR_TOP_LIST_DEEPSPACE})
    session = Session(timescale=ts,
                      start=now,
                      end=now,
                      latitude=location.latitude,
                      longitude=location.longitude,
                      altitude=location.altitude,
                      min_alt=0.0,
                      max_alt=90,
                      min_az=None,
                      max_az=None,
                      constellation=None,  # E.g. 'Virgo'
                      only_kind=None,  # E.g. 'Galaxy'
                      min_apparent_mag=None,
                      only_from_catalog='NGC',  # NGC, IC, or Messier
                      only_these_sources=None,  # A dictionary of the top lists, from constants
                      limit=500)  # None for no limit, an integer to limit the number of results, for faster completion.

    # session.log_visible() # DEBUG
    print('Here are some interesting objects up in the sky right now:')
    print('\n  Solar system:'.upper())

    if session.objects_visible_now.planets:
        for obj in session.objects_visible_now.planets:
            obj.update_coords()
            # print(obj.name, obj.alt, obj.az, obj.distance)
            print(f'   • {obj.name.ljust(7)} {obj.alt.degrees:8.4f} {obj.az.degrees:7.4f}, {obj.distance.au:5.1f}au')
    else:
        print('[Nothing to show here]')

    print('\n  Deep space objects:'.upper())
    if session.objects_visible_now.deepspace:
        for obj in session.objects_visible_now.deepspace:
            obj.update_coords()
            # print(obj.name, obj.alt, obj.az, obj.distance)
            print(f'   • {obj.name.ljust(7)} {obj.alt.degrees:8.4f} {obj.az.degrees:7.4f}, {obj.distance.au:5.1f}au')
    else:
        print('   • [Nothing to show here]')

    print('\n')


if __name__ == "__main__":
    main()
