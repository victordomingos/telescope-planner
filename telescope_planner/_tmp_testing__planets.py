#!/usr/bin/env python3
from skyfield.api import load, Star, Topos
from pytz import timezone

from geocode import get_location, DEFAULT_LOCATION

planets = load('de421.bsp')
earth = planets['earth']

all_planets = [
    'sun', 'mercury', 'venus', 'earth', 'moon', 'mars', 'JUPITER BARYCENTER',
    'URANUS BARYCENTER', 'NEPTUNE BARYCENTER', 'PLUTO BARYCENTER'
]

stars = [('Polaris', (2, 55, 16), (89, 20, 58)),
         ('barnard', (17, 57, 48.49803), (4, 41, 36.2072))]

# cur_place, _ = get_location()  # Todo: Remove comment before release
cur_place = DEFAULT_LOCATION  # DEBUG
ts = load.timescale()
t = ts.now()
here = earth + Topos(f'{cur_place.latitude} N', f'{cur_place.longitude} E')

print('\n\n\n')
print(f'{cur_place.city} {cur_place.latitude:.5f}N, {cur_place.longitude:.5f}E\n')
print('UTC:  ', t.utc_datetime())
tz = timezone('Europe/Lisbon')
# tz = timezone('NZ')
print('Local:', t.astimezone(tz), '\n')

print('\n\nSolar System:')
print('=============\n')


def is_planet_up(planet, latitude, longitude, time):
    here = earth + Topos(f'{latitude} N', f'{longitude} E')
    p = planets[planet]
    planet_astro = here.at(t).observe(p)
    planet_app = planet_astro.apparent()
    alt, az, d = planet_app.altaz('standard')

    planet_name = planet.split()[0].upper()
    if alt.degrees > 0.0:
        is_up = True
        # print(f'{planet_name}:\n', '    ALT:', alt, '\n     AZ:', az)
    else:
        is_up = False
        # out_of_sight.append(planet_name)
    return is_up, alt.degrees, az.degrees, d.au


out_of_sight = []
for planet in all_planets:
    if planet.upper() == 'EARTH':
        continue
    up, alt, az, d = is_planet_up(planet, cur_place.latitude,
                                  cur_place.longitude, t)
    planet_name = planet.split()[0].upper()

    if up:
        # print(f'{planet_name.ljust(7)}:\n', '    ALT:', alt, '\n     AZ:', az)
        print(f'{planet_name.ljust(7)} {str(up).ljust(5)} {alt:8.4f} {az:7.4f}, {d:.1f}au')
    else:
        out_of_sight.append(planet_name)

if out_of_sight:
    print('\nThese are not visible:')
    print(', '.join(out_of_sight))


"""
print('\n\nStars and other deep sky objects:')
print('=================================\n')

out_of_sight_stars = []
for name, ra_hours, dec_degrees in stars:
    star_obj = Star(ra_hours=ra_hours, dec_degrees=dec_degrees)
    star_astro = here.at(t).observe(star_obj)
    star_app = star_astro.apparent()
    alt, az, d = star_app.altaz('standard')

    if alt.degrees > 0.0:
        print(f'{name.upper()}:\n', '    ALT:', alt, '\n     AZ:', az)
    else:
        out_of_sight_stars.append(name.upper())

if out_of_sight_stars:
    print('\nThese are not visible:')
    print(', '.join(out_of_sight_stars))
"""