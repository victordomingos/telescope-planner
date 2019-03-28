#!/usr/bin/env python3
from telescope_planner.constants import DEFAULT_LOCATION, NOW


def get_next_sunset(when=NOW):
    pass


def get_next_sunrise(when=NOW):
    pass


class Session():
    def __init__(self, start=get_next_sunset(), end=get_next_sunrise(), latitude=DEFAULT_LOCATION.latitude,
                 longitude=DEFAULT_LOCATION.longitude, min_alt=0.0, max_alt=90, min_az=None, max_az=None,
                 constellation=None, min_apparent_mag=None, using_catalogs=None):
        self.start = start
        self.end = end

        # user/observatory location:
        self.latitude = latitude
        self.longitude = longitude

        # minimum altitude/azimute that will be used in this session (depending
        # for instance on the telescope mount angles or any physical obstacles on the observatory):
        self.min_alt = min_alt
        self.max_alt = max_alt
        self.min_az = min_az
        self.max_az = max_az

        # restrict current session to objects that are inside or near a specific constellation:
        self.constellation = constellation

        # restrict current session to objects with apparent magnitude greater than:
        self.min_apparent_mag = min_apparent_mag

        # restrict current session to objects in these catalogs:
        self.using_catalogs = using_catalogs if using_catalogs is not None else []

        self.objects_visible = []
        self.objects_not_visible = []
        self.objects_not_defined = []

        planets = load('de421.bsp')
        earth = planets['earth']
        here = earth + Topos(f'{location.latitude} N', f'{location.longitude} E')
        solar_system = [ PlanetObserver(name, here, NOW)
                         for name in SOLAR_SYSTEM]



    def __repr__(self):
        super().__repr__()

    def __str__(self):
        super().__str__()
