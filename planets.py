from skyfield.api import load, Topos

from geocode import get_location, DEFAULT_LOCATION

planets = load('de421.bsp')
earth = planets['earth']

all_planets = [
    'sun', 'mercury', 'venus', 'earth', 'moon', 'mars', 'JUPITER BARYCENTER',
    'URANUS BARYCENTER', 'NEPTUNE BARYCENTER', 'PLUTO BARYCENTER'
]

current_place, _ = get_location()
ts = load.timescale()
t = ts.now()

print('\n======================')
print(
    f'{current_place.city} {current_place.latitude:.5f}N, {current_place.longitude:.5f}E\n'
)
print(t.utc_datetime(), '\n')

here = earth + Topos(f'{current_place.latitude} N',
                     f'{current_place.longitude} E')

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