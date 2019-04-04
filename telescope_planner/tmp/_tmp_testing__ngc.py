#!/usr/bin/env python3
from pyongc import ongc
from skyfield.api import load, Star, Topos

from telescope_planner.geocode import get_location, DEFAULT_LOCATION

# cur_place, _ = get_location()
cur_place = DEFAULT_LOCATION
ts = load.timescale()
t = ts.now()

planets = load('de421.bsp')
earth = planets['earth']

if cur_place.altitude is None:
    print(f'  Alt.: <undetermined>')
    altitude = '0.0'
else:
    print(f'  Alt.: {cur_place.altitude:.0f}m\n')
    altitude = cur_place.altitude

here = earth + Topos(latitude=f'{cur_place.latitude} N', longitude=f'{cur_place.longitude} E', elevation_m=cur_place.altitude)

star_names = ['NGC' + str(i) for i in range(1, 7001)]




"""
print('Phase 1')
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
        #print(e)
        pass

report = f'Currently visible stars and other deep sky objects:\n'
print(report + len(report) * '=')

out_of_sight_stars = []
visible_stars = ''
vis_stars_list = []
error_stars_list = []
messier_list = []
messier_out_list = []
messier_errors = []



print('Phase 2')
for name in star_names:
    try:
        DSOobject = ongc.Dso(name)
        ra_arr, dec_arr = DSOobject.getCoords()
        ra, dec = tuple(ra_arr), tuple(dec_arr)
        alt_ids = DSOobject.getIdentifiers()
        messier = alt_ids[0]
        #if messier is None:
        #    messier = 'N/A'
        constellation = DSOobject.getConstellation()
        obj_type = DSOobject.getType()
        # print('\nids:', alt_ids)

        star_obj = Star(ra_hours=ra, dec_degrees=dec)
        star_astro = here.at(t).observe(star_obj)
        star_app = star_astro.apparent()
        alt, az, d = star_app.altaz('standard')

        if alt.degrees > 0.0:
            #print(f'\n{name.upper()} ({messier}) - {obj_type}:\n  ALT: {alt}\n   AZ: {az}\n   Constellation:', constellation)
            visible_stars = visible_stars + f'\n{name.upper()} ({messier}) - {obj_type}:\n  ALT: {alt}\n   AZ: {az}\n   Constellation: {constellation})\n'
            vis_stars_list.append(name.upper)
            if messier:
                messier_list.append((name,messier))
        else:
            out_of_sight_stars.append(name.upper())
            if messier:
                messier_out_list.append((name,messier))
    except ValueError as e:
        #out_of_sight_stars.append(name.upper())
        error_stars_list.append(name.upper())
        #print(e)
        if messier:
            messier_errors.append((name, messier))
            
print(f'\n\n{len(vis_stars_list)} currently visible')
#print(reports + len(report) * '=')

if out_of_sight_stars:
    report2 = f'\n\n{len(out_of_sight_stars)} currently not visible:\n'
    print(report2 + len(report) * '=')
    #print(', '.join(out_of_sight_stars))
    
if error_stars_list:
    print('Some kind of error ocurred on these:')
    print(error_stars_list)

print('Visible Messier objects: ', len(messier_list))
print(messier_list)

print('These messier objects are out of sight:', len(messier_out_list))
print(messier_out_list)

print(f'There is some issue with these {len(messier_errors)} messier items:')
print(messier_errors)

"""

print('Phase 3')
from pyongc.ongc import listObjects

from telescope_planner.constants import ONGC_CATALOGS_ABREVS_FROM_NAMES, CONSTELLATIONS_ABBREV_FROM_LATIN
from telescope_planner.constants import ONGC_TYPES_ABREVS_FROM_NAMES


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_dso_list(catalog=None, kind=None, constellation=None, uptovmag=None, limit=None):
    params = dict()

    if (catalog is not None) and (catalog in ONGC_CATALOGS_ABREVS_FROM_NAMES.keys()):
        params.update({'catalog': ONGC_CATALOGS_ABREVS_FROM_NAMES[catalog]})

    if (kind is not None) and (kind in ONGC_TYPES_ABREVS_FROM_NAMES.keys()):
        params.update({'type': ONGC_TYPES_ABREVS_FROM_NAMES[kind]})

    if (constellation is not None) and (constellation in CONSTELLATIONS_ABBREV_FROM_LATIN.keys()):
        params.update({'constellation': CONSTELLATIONS_ABBREV_FROM_LATIN[constellation]})

    if uptovmag is not None and is_float(uptovmag):
        params.update({'uptovmag': float(uptovmag)})

    # print(params) # DEBUG
    return [obj for obj in listObjects(**params)[0:limit]
            if obj.getType() != "Duplicated record"]


# Define a rectangular constraint using the location alt/az, using decimal degrees:
min_alt = .0
max_alt = 90.0
min_az = .0
max_az = 360.0


"""
bottom_left_star =
top_right_star =
"""





from skyfield import api

ts = api.load.timescale()
planets = api.load('de421.bsp')
earth = planets['earth']

here = earth + api.Topos(latitude=f'{cur_place.latitude} N',
                         longitude=f'{cur_place.longitude} E',
                         elevation_m=cur_place.altitude)

t = ts.now()

dir = here.at(t).from_altaz(alt_degrees=41.1, az_degrees=180)
ra, dec, distance = dir.radec()

print("RA:", ra)
print("DEC:", dec)



# Define a rectangle constraint using ra/dec for current location/datetime:
min_alt = min_alt
max_alt = max_alt
min_az = min_az
max_az = max_az






"""
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
        # print(e)
        pass

report = f'Currently visible stars and other deep sky objects:\n'
print(report + len(report) * '=')

out_of_sight_stars = []
visible_stars = ''
vis_stars_list = []
error_stars_list = []
messier_list = []
messier_out_list = []
messier_errors = []

print('Phase 2B')
for name in star_names:
    try:
        DSOobject = ongc.Dso(name)
        ra_arr, dec_arr = DSOobject.getCoords()
        ra, dec = tuple(ra_arr), tuple(dec_arr)
        alt_ids = DSOobject.getIdentifiers()
        messier = alt_ids[0]
        # if messier is None:
        #    messier = 'N/A'
        constellation = DSOobject.getConstellation()
        obj_type = DSOobject.getType()
        # print('\nids:', alt_ids)

        star_obj = Star(ra_hours=ra, dec_degrees=dec)
        star_astro = here.at(t).observe(star_obj)
        star_app = star_astro.apparent()
        alt, az, d = star_app.altaz('standard')

        if alt.degrees > 0.0:
            # print(f'\n{name.upper()} ({messier}) - {obj_type}:\n  ALT: {alt}\n   AZ: {az}\n   Constellation:', constellation)
            visible_stars = visible_stars + f'\n{name.upper()} ({messier}) - {obj_type}:\n  ALT: {alt}\n   AZ: {az}\n   Constellation: {constellation})\n'
            vis_stars_list.append(name.upper)
            if messier:
                messier_list.append((name, messier))
        else:
            out_of_sight_stars.append(name.upper())
            if messier:
                messier_out_list.append((name, messier))
    except ValueError as e:
        # out_of_sight_stars.append(name.upper())
        error_stars_list.append(name.upper())
        # print(e)
        if messier:
            messier_errors.append((name, messier))

print(f'\n\n{len(vis_stars_list)} currently visible')
# print(reports + len(report) * '=')

if out_of_sight_stars:
    report2 = f'\n\n{len(out_of_sight_stars)} currently not visible:\n'
    print(report2 + len(report) * '=')
    # print(', '.join(out_of_sight_stars))

if error_stars_list:
    print('Some kind of error ocurred on these:')
    print(error_stars_list)

print('Visible Messier objects: ', len(messier_list))
print(messier_list)

print('These messier objects are out of sight:', len(messier_out_list))
print(messier_out_list)

print(f'There is some issue with these {len(messier_errors)} messier items:')
print(messier_errors)
"""