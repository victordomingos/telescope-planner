#!/usr/bin/env python3
from pyongc import ongc
from skyfield.api import load, Star, Topos

from geocode import get_location, DEFAULT_LOCATION

# cur_place, _ = get_location()
cur_place = DEFAULT_LOCATION
ts = load.timescale()
t = ts.now()

planets = load('de421.bsp')
earth = planets['earth']
here = earth + Topos(f'{cur_place.latitude} N', f'{cur_place.longitude} E')

star_names = ['NGC' + str(i) for i in range(1, 7000)]

stars = []
for name in star_names:
    try:
        DSOobject = ongc.Dso(name)
        ra_arr, dec_arr = DSOobject.getCoords()
        ra, dec = tuple(ra_arr), tuple(dec_arr)
        alt_ids = DSOobject.getIdentifiers()
        messier = alt_ids[0]
        constellation = DSOobject.getConstellation()
        obj_type = DSOobject.getType()
        # print('\nids:', alt_ids)
        stars.append((name, ra, dec))
    except ValueError as e:
        print(e)

report = f'\n\n{len(stars)} currently visible stars and other deep sky objects:\n'
print(report + len(report) * '=')

out_of_sight_stars = []
for name in star_names:
    try:
        DSOobject = ongc.Dso(name)
        ra_arr, dec_arr = DSOobject.getCoords()
        ra, dec = tuple(ra_arr), tuple(dec_arr)
        alt_ids = DSOobject.getIdentifiers()
        messier = alt_ids[0]
        if messier is None:
            messier = 'N/A'
        constellation = DSOobject.getConstellation()
        obj_type = DSOobject.getType()
        # print('\nids:', alt_ids)

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
    except ValueError as e:
            print(e)

if out_of_sight_stars:
    report2 = f'\n\n{len(out_of_sight_stars)} currently not visible:\n'
    print(report2 + len(report) * '=')
    print(', '.join(out_of_sight_stars))
