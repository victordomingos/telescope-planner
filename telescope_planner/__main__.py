#!/usr/bin/env python3
"""
A simple utility for telescope time planning, for astronomy hobbyists. The aim
is to provide an easy to use tool to help planning sky observation sessions,
suggesting some of the interesting objects you may be able to watch at naked
eye, or using amateur equipment (binoculars or small to medium size telescopes)
in a given date/time and place.

© 2019 Victor Domingos (MIT License)
"""
import logging
import sys

from pprint import pformat
from types import SimpleNamespace

from skyfield.api import Loader
from pytz import timezone

from telescope_planner.constants import OUR_TOP_LIST_PLANETS, OUR_TOP_LIST_DEEPSPACE
from telescope_planner.constants import DEFAULT_LOCATION, CONSTELLATIONS_LATIN_FROM_ABBREV
from telescope_planner.settings import DATA_FOLDER, DEFAULT_MIN_MAG, NAKED_EYE_MAG
from telescope_planner.geocode import get_location
from telescope_planner.session import Session


def main():
    logging.basicConfig(level=logging.DEBUG,
                        datefmt='%Y-%b-%d %H:%M:%S',
                        format='%(asctime)s %(levelname)s P%(process)d T%(thread)d %(filename)s L%(lineno)d %(funcName)s() - %(message)s %(relativeCreated)d ms')

    s = " Welcome to Telescope Planner! "
    line = len(s) * '='
    print(f'\n{line}\n{s}\n{line}')

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
        altitude = '0'
    else:
        print(f'  Alt.: {location.altitude:.0f}m\n')
        altitude = location.altitude


    # TODO: The sources variable can be initialized with a list of Messier IDs, for instance
    sources = SimpleNamespace(**{'planets': OUR_TOP_LIST_PLANETS,
                                 'deepspace': OUR_TOP_LIST_DEEPSPACE})
    session_params = {'timescale': ts,
                      'start': now,
                      'end': now,
                      'latitude': location.latitude,
                      'longitude': location.longitude,
                      'altitude': altitude,
                      'min_alt': 0.0,
                      'max_alt': 90.0,
                      'min_az': 0.0,
                      'max_az': 360.0,
                      'constellation': 'Peg',  # E.g. 'Virgo', 'Leo'
                      'only_kind': None,  # E.g. 'Galaxy', 'Nebula'…
                      # ~14.5 for the average 8-10inch telescope (DEFAULT_MIN_MAG)
                      # ~6 for naked eye with little light pollution (NAKED_EYE_MAG):
                      'min_apparent_mag': DEFAULT_MIN_MAG,
                      'only_from_catalog': None,  # NGC, IC, or Messier
                      'only_these_sources': None,  # A dictionary of the top lists, from module constants
                      # None for no limit, an integer to limit the number of results, for faster completion:
                      'limit': 100,
                      }

    logging.debug(pformat(session_params))

    logging.debug("New session")

    session = Session(**session_params)
    logging.debug("Finalized Session initialization. Starting report generation.")
    print('Here are some interesting objects up in the sky right now:')
    print('\n  Solar system:'.upper())

    if session.objects_visible_now.planets:
        for obj in session.objects_visible_now.planets:
            obj.update_coords()
            # print(obj.name, obj.alt, obj.az, obj.distance)
            print(f'   • {obj.name.ljust(17)} Alt: {obj.alt.degrees:8.4f} Az: {obj.az.degrees:8.4f}, D: {obj.distance.au:15.1f}au - {obj.kind}')
    else:
        print('[Nothing to show here]')

    print('\n  Deep space objects:'.upper())
    logging.debug("Starting deep space report generation.")
    if session.objects_visible_now.deepspace:
        for obj in session.objects_visible_now.deepspace:
            obj.update_coords()
            # print(obj.name, obj.alt, obj.az, obj.distance)
            print(f'   • {obj.name.ljust(17)}    Alt: {obj.alt.degrees:8.4f} Az: {obj.az.degrees:8.4f} - {obj.kind} in {CONSTELLATIONS_LATIN_FROM_ABBREV[obj.constellation]}')
        print('\n  ', len(session.objects_visible_now.deepspace), "objects visible from a total of",
              len(session.deepspace_selection), "objects analyzed.")
    else:
        print('   • [Nothing to show here]')

    logging.debug("Finalized report presentation.")
    print('\n')


if __name__ == "__main__":
    main()
