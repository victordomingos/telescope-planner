from skyfield.api import load, Star, Topos

from geocode import get_location

planets = load('de421.bsp')
earth = planets['earth']

all_planets = [
    'sun', 'mercury', 'venus', 'earth', 'moon', 'mars', 'JUPITER BARYCENTER',
    'URANUS BARYCENTER', 'NEPTUNE BARYCENTER', 'PLUTO BARYCENTER'
]

stars = [('Polaris', (2, 55, 16), (89, 20, 58)),
         ('barnard', (17, 57, 48.49803), (4, 41, 36.2072))]

cur_place, _ = get_location()
ts = load.timescale()
t = ts.now()
here = earth + Topos(f'{cur_place.latitude} N', f'{cur_place.longitude} E')


print('\n\n\n')
print(f'{cur_place.city} {cur_place.latitude:.5f}N, {cur_place.longitude:.5f}E\n')
print(t.utc_datetime(), '\n')

print('\n\nSolar System:')
print('=============\n')

out_of_sight = []
for planet in all_planets:
    if planet.upper() == 'EARTH':
        continue
    p = planets[planet]
    planet_astro = here.at(t).observe(p)
    planet_app = planet_astro.apparent()
    alt, az, d = planet_app.altaz('standard')

    if alt.degrees > 0.0:
        print(f'{planet.upper()}:\n', '    ALT:', alt, '\n     AZ:', az)
    else:
        out_of_sight.append(planet.upper())

print('\nThese are not visible:')
print(', '.join(out_of_sight))

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

print('\nThese are not visible:')
print(', '.join(out_of_sight_stars))