#!/usr/bin/env python3
from pyongc import ongc
from skyfield.api import load, Star, Topos

from geocode import get_location

cur_place, _ = get_location()
ts = load.timescale()
t = ts.now()

planets = load('de421.bsp')
earth = planets['earth']
here = earth + Topos(f'{cur_place.latitude} N', f'{cur_place.longitude} E')

star_names = ['NGC7000', 'NGC4548']

stars = []
for name in star_names:
    DSOobject = ongc.Dso(name)
    ra_arr, dec_arr = DSOobject.getCoords()
    ra, dec = tuple(ra_arr), tuple(dec_arr)
    alt_ids = DSOobject.getIdentifiers()
    messier = alt_ids[0]
    constellation = DSOobject.getConstellation()
    obj_type = DSOobject.getType()
    #print('\nids:', alt_ids)
    stars.append((name, ra, dec))

print('\n\nStars and other deep sky objects:')
print('=================================')

out_of_sight_stars = []
for name in star_names:
    DSOobject = ongc.Dso(name)
    ra_arr, dec_arr = DSOobject.getCoords()
    ra, dec = tuple(ra_arr), tuple(dec_arr)
    alt_ids = DSOobject.getIdentifiers()
    messier = alt_ids[0]
    if messier is None:
        messier = 'N/A'
    constellation = DSOobject.getConstellation()
    obj_type = DSOobject.getType()
    #print('\nids:', alt_ids)

    star_obj = Star(ra_hours=ra, dec_degrees=dec)
    star_astro = here.at(t).observe(star_obj)
    star_app = star_astro.apparent()
    alt, az, d = star_app.altaz('standard')

    if alt.degrees > 0.0:
        print(f'\n{name.upper()} ({messier}) - {obj_type}:\n', '  ALT:', alt,
              '\n   AZ:', az)
        print('   Constellation:', constellation)
    else:
        out_of_sight_stars.append(name.upper())

if out_of_sight_stars:
    print('\nThese are not visible:')
    print(', '.join(out_of_sight_stars))
