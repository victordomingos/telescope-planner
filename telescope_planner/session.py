#!/usr/bin/env python3
from types import SimpleNamespace

from skyfield.api import Loader, Topos

from telescope_planner.constants import DEFAULT_LOCATION, NOW, SOLAR_SYSTEM
from telescope_planner.geocode import get_location
from telescope_planner.settings import DATA_FOLDER
from telescope_planner.observers import PlanetObserver, DeepSpaceObserver


def get_next_sunset(when=NOW):
    pass


def get_next_sunrise(when=NOW):
    pass


class Session():
    def __init__(self, start=None, end=None, latitude=DEFAULT_LOCATION.latitude,
                 longitude=DEFAULT_LOCATION.longitude, altitude=DEFAULT_LOCATION.altitude, min_alt=0.0, max_alt=90,
                 min_az=None, max_az=None,
                 constellation=None, min_apparent_mag=None, using_catalogs=None):
        self.start = start if start is not None else get_next_sunset()
        self.end = end if end is not None else get_next_sunrise()

        # user/observatory location:
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

        # minimum altitude/azimuth that will be used in this session (depending
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

        self.objects_visible = SimpleNamespace(**{'planets': [], 'deepspace': []})
        self.objects_not_visible = SimpleNamespace(**{'planets': [], 'deepspace': []})
        self.objects_not_defined = SimpleNamespace(**{'planets': [], 'deepspace': []})

        load = Loader(DATA_FOLDER)
        self.planets = load('de421.bsp')
        self.earth = self.planets['earth']
        self.here = None

        self.update_user_location(self.latitude, self.longitude)

        self.solar_system = [PlanetObserver(name, self)
                             for name in SOLAR_SYSTEM]
        self.update_solar_objects()
        self.update_deepspace_objects()

    def log_visible(self):
        print(len(self.objects_visible.planets), "visible solar system objects:")
        for obj in self.objects_visible.planets:
            print(obj)

    def check_user_location(self):
        """Try to determine user location, using network or GPS."""
        location, source = get_location()
        self.update_user_location(location.latitude, location.longitude)

    def update_user_location(self, latitude: float, longitude: float):
        """Set the new coordinates for the observatory and then update any
        values that depend on the user location."""
        self.latitude = latitude
        self.longitude = longitude
        self.here = self.earth + Topos(f'{self.latitude} N', f'{self.longitude} E')
        # TODO: update anything that depends on the user location

    def update_solar_objects(self):
        """ Update coordinates and other properties for all visible objects """
        self.objects_visible.planets = []
        self.objects_not_visible.planets = []
        self.objects_not_defined.planets = []
        for obj in self.solar_system:
            obj.update_altaz()
            if obj.is_up():
                self.objects_visible.planets.append(obj)
            else:
                self.objects_not_visible.planets.append(obj)

    def update_deepspace_objects(self):
        """ Update coordinates and other properties for all visible objects """
        self.objects_visible.deepspace = []
        self.objects_not_visible.deepspace = []
        self.objects_not_defined.deepspace = []
        """ TODO:
        for obj in self.solar_system:
            obj.update_altaz()
            if obj.is_up():
                self.objects_visible.deepspace.append(obj)
            else:
                self.objects_not_visible.deepspace.append(obj)
        """

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f'<{cls_name}: Lat.{self.latitude}, Long.{self.longitude} | {self.start.utc_datetime()}>'

    def __str__(self):
        cls_name = self.__class__.__name__
        return f'<{cls_name}: Lat.{self.latitude}, Long.{self.longitude} | {self.start.utc_datetime()}>'
