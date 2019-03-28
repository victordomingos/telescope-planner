#!/usr/bin/env python3
"""
A simple utility for telescope time planning, for astronomy hobbyists. The aim
is to provide an easy to use tool to help planning sky observation sessions,
suggesting some of the interesting objects you may be able to watch at naked
eye, or using amateur equipment (binoculars or small to medium size telescopes)
in a given date/time and place.

© 2019 Victor Domingos (MIT License)
"""

from telescope_planner.geocode import get_location, DEFAULT_LOCATION
from telescope_planner.observers import PlanetObserver, DeepSpaceObserver, SOLAR_SYSTEM
from telescope_planner.session import Session

if __name__ == "__main__":
    # location, source = get_location()
    location, source = DEFAULT_LOCATION, "DEBUG method"

    print(f'\nBased on the {source}, this is your current location:\n')
    print(f'  {location.dms_latitude} {location.dms_longitude}\n  {location.city}, {location.country}')
    if location.altitude is None:
        print(f'  Alt.: <undetermined>')
    else:
        print(f'  Alt.: {location.altitude:.0f}m\n')

    session = Session()
    solar_system = []
    for name in SOLAR_SYSTEM:
        planet = PlanetObserver(name, location.latitude, location.longitude)
        print(planet)
        solar_system.append(planet)

    print(len(solar_system), "Solar System objects.")
