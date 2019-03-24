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
print("Estimated elevation: {altitude}m.")

location = Observer(longitude=here.longitude * u.deg,
                    latitude=here.latitude * u.deg,
                    elevation=altitude * u.m,
                    timezone='Europe/Lisbon')

print("Is it night at your observatory?", location.is_night(time))

# star_names = ['NGC' + str(i) for i in range(1, 7000)]
star_names = ['M' + str(i) for i in range(1, 111)]


def show_star_info(obj):
    star = FixedTarget.from_name(obj)
    print("\n", obj, star)
    rise_time = location.target_rise_time(time, star)
    print('Rise time:', rise_time)
    #altitude_at_rise = location.altaz(rise_time, star).alt
    #print('Altitude at rise:', altitude_at_rise.to('arcsec'))


for i, obj in enumerate(star_names):
    show_star_info(obj)
    if i > 0 and i % 5 == 0:
        print("Pausing...")
        sleep(10)
