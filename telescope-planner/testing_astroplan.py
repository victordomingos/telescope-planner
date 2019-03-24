import datetime
import geocode
import astropy.units as u
from astroplan import Observer, FixedTarget
from astropy.time import Time
from time import sleep

# from astroplan import download_IERS_A
# download_IERS_A()

time = Time(datetime.datetime.now())

planets = [
    'mercury', 'venus', 'earth', 'moon', 'mars', 'JUPITER BARYCENTER',
    'URANUS BARYCENTER', 'NEPTUNE BARYCENTER', 'PLUTO BARYCENTER'
]

deek_sky_objects = ['Altair', 'Vega', 'NGC7000', 'deneb', 'Polaris', 'M105', ]

# stars = [('Polaris', (2, 55, 16), (89, 20, 58)),
#         ('barnard', (17, 57, 48.49803), (4, 41, 36.2072))]

print("Getting current location…")
here, location_source = geocode.get_location()

if here.altitude is None:
    altitude = 0
else:
    altitude = here.altitude

print(f"Detected location using {location_source}.")
print(f"You're near {here.city} (coords: {here.longitude} {here.latitude}.")
print(f"Estimated elevation: {altitude}m.")

location = Observer(longitude=here.longitude * u.deg,
                    latitude=here.latitude * u.deg,
                    elevation=altitude * u.m,
                    timezone='Europe/Lisbon')

print("Is it night at your observatory?", location.is_night(time))

# star_names = ['NGC' + str(i) for i in range(1, 7000)]
star_names = ['M' + str(i) for i in range(1, 111)]


def get_star_info(obj):
    star = FixedTarget.from_name(obj)
    is_up = location.target_is_up(time, star)

    if not is_up:
        return None, None, None, is_up

    rise_time = location.target_rise_time(time, star)
    set_time = location.target_set_time(time, star)
    altitude_at_rise = location.altaz(rise_time, star).alt
    return rise_time, set_time, altitude_at_rise, is_up


messier_list = []
messier_not_visible = []
messier_error_list = []
for i, obj in enumerate(star_names):
    if i > 0 and i % 5 == 0:
        print("Pausing...")
        sleep(10)

    rtime, stime, alt_at_rise, up = get_star_info(obj)
    if not up or alt_at_rise < 0:  # TODO: fix this - we need to check if the object will be up during the interval of time, not at current time…
        messier_not_visible.append(obj)
        continue
    print(f"\n{obj}")
    try:
        print("RTime", location.astropy_time_to_datetime(rtime))
        print("STime", location.astropy_time_to_datetime(stime))
        print("AltRise:", alt_at_rise.to('arcsec'))
        messier_list.append(obj)
    except ValueError as ve:
        messier_error_list.append(obj)
        print(ve)
    except Exception as e:
        messier_error_list.append(obj)
        print(e)



print(f"Currently these {len(messier_list)} Messier objects are up in the sky: ")
print(messier_list)
