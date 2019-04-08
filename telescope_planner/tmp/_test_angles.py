#!/usr/bin/env python3
from pyongc.ongc import listObjects
from skyfield.api import load, Topos
from skyfield.units import Angle as SF_Angle
from types import SimpleNamespace

DEFAULT_LOCATION = SimpleNamespace(**{
    'latitude': 41.55926513671875,
    'longitude': -8.405625509894655,
    'altitude': 190.0,
})

min_alt = -90.0
max_alt = 90.0
min_az = 0.0
max_az = 360.0


def get_dso_list():
    return [obj for obj in listObjects(catalog='M')
            if obj.getType() != "Duplicated record" and obj.getType() != "Nonexistent object"]


def radec2deg(ra='', dec=''):
    """ Convert right ascension/declination from strings to decimal degrees.

    Takes RA and/or Dec from strings in HH:MM:SS format and DD:MM:SS,
    respectively. Each coordinate is converted to a decimal degrees float.
    In case both parameters are provided, it returns a tuple.
    """
    dec_deg = None
    ra_sign = 1
    ra_deg = None
    dec_sign = 1

    if dec:
        degs, mins, secs = [float(i) for i in dec.split(sep=':')]
        if str(degs)[0] == '-':
            dec_sign = -1
            degs = abs(degs)
        dec_deg = dec_sign * (degs + (mins / 60) + (secs / 3600))

    if ra:
        hours, mins, secs = [float(i) for i in ra.split(':')]
        if str(hours)[0] == '-':
            ra_sign, hours = -1, abs(hours)
        deg = (hours * 15) + (mins / 4) + (secs / 240)
        ra_deg = deg * ra_sign

    if ra and dec:
        return ra_deg, dec_deg
    else:
        return ra_deg or dec_deg


def is_inside_window2(obj, min_ra, min_dec, max_ra, max_dec):
    ra, dec = radec2deg(ra=obj.getRA(), dec=obj.getDec())
    ra_angle = SF_Angle(degrees=ra)
    dec_angle = SF_Angle(degrees=dec)

    print("\n======", obj.getName(), obj.getIdentifiers(), "======")
    print(f"OBJ RA {ra_angle.degrees}  /  OBJ DEC {dec_angle.degrees}")
    print(f"minRA  {min_ra._degrees}°  /  MAXRA   {max_ra._degrees}°")
    print(f"minDEC {min_dec.degrees}°  /  MAXDEC  {max_dec.degrees}°")

    if not (min_ra._degrees <= ra_angle._degrees <= max_ra._degrees):
        print(" - RA FALSE!")
        return False
    if not (min_dec.degrees <= dec_angle.degrees <= max_dec.degrees):
        print(" - DEC FALSE!")
        return False
    print(" - Both RA and DEC are within bounds!")
    return True


planets = load('de421.bsp')
earth = planets['earth']
here = earth + Topos(latitude=DEFAULT_LOCATION.latitude,
                     longitude=DEFAULT_LOCATION.longitude,
                     elevation_m=DEFAULT_LOCATION.altitude)
selection = get_dso_list()

ts = load.timescale()
moment = ts.now()

min_ra, min_dec, _ = here.at(moment).from_altaz(alt_degrees=min_alt, az_degrees=min_az).radec()
max_ra, max_dec, _ = here.at(moment).from_altaz(alt_degrees=max_alt, az_degrees=max_az).radec()
selection_filtered = []
filtered_out = []

for obj in selection:
    selection_filtered = [obj for obj in selection
                          if is_inside_window2(obj, min_ra, min_dec, max_ra, max_dec)]

    filtered_out = [obj for obj in selection
                    if not is_inside_window2(obj, min_ra, min_dec, max_ra, max_dec)]

print("\n\nFor some reason, these objects are not included:\n")

for obj in filtered_out:
    print(obj.getName(), obj.getRA(), obj.getDec(), obj.getType(), obj.getIdentifiers())

print("\nTotal objects considered:   ", len(selection))
print("Within the specified window:", len(selection_filtered))
print("Out of the specified window:", len(filtered_out))
