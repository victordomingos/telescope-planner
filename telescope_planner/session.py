#!/usr/bin/env python3
from types import SimpleNamespace

from skyfield.api import Loader, Topos
from pyongc import Dso, listObjects

from telescope_planner.constants import DEFAULT_LOCATION, SOLAR_SYSTEM
from telescope_planner.geocode import get_location
from telescope_planner.settings import DATA_FOLDER
from telescope_planner.observers import PlanetObserver, DeepSpaceObserver

"""
def get_next_sunset(when=NOW):
    pass


def get_next_sunrise(when=NOW):
    pass
"""


class Session():
    def __init__(self, timescale=None, start=None, end=None, latitude=DEFAULT_LOCATION.latitude,
                 longitude=DEFAULT_LOCATION.longitude, altitude=DEFAULT_LOCATION.altitude, min_alt=0.0, max_alt=90,
                 min_az=None, max_az=None,
                 constellation=None, min_apparent_mag=None, using_catalogs=None, from_list=None):
        self.start = start if start is not None else get_next_sunset()
        self.end = end if end is not None else get_next_sunrise()

        self.ts = timescale

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
        self.from_list = from_list

        self.objects_visible_now = SimpleNamespace(**{'planets': [], 'deepspace': []})
        self.objects_not_visible = SimpleNamespace(**{'planets': [], 'deepspace': []})
        self.objects_not_defined = SimpleNamespace(**{'planets': [], 'deepspace': []})

        self.objects_visible_during_session = SimpleNamespace(**{'planets': [], 'deepspace': []})
        self.objects_not_visible_during_session = SimpleNamespace(**{'planets': [], 'deepspace': []})
        self.objects_not_defined_during_session = SimpleNamespace(**{'planets': [], 'deepspace': []})

        load = Loader(DATA_FOLDER)
        self.planets = load('de421.bsp')
        self.earth = self.planets['earth']
        self.here = None

        self.update_user_location(self.latitude, self.longitude)

        if self.from_list.planets:
            self.solar_system = [PlanetObserver(name, self)
                                 for name in self.from_list.planets]
        else:
            self.solar_system = [PlanetObserver(name, self)
                                 for name in SOLAR_SYSTEM]

        if self.from_list.deepspace:
            self.deepspace_selection = [DeepSpaceObserver(name, self)
                                        for name in self.from_list.deepspace]
        else:
            self.deepspace_selection = []

        self.update_now_solar_objects()
        self.update_now_deepspace_objects()

    def log_visible(self):
        print(len(self.objects_visible_now.planets), "visible solar system objects:")
        for obj in self.objects_visible_now.planets:
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

    def update_now_solar_objects(self):
        """ Update current coordinates and other properties for all visible objects """
        self.objects_visible_now.planets = []
        self.objects_not_visible.planets = []
        self.objects_not_defined.planets = []
        for obj in self.solar_system:
            obj.update_coords()
            if obj.is_up_now():
                self.objects_visible_now.planets.append(obj)
            else:
                self.objects_not_visible.planets.append(obj)

    def generate_session_list(self):
        self.objects_visible_during_session.planets = []
        self.objects_not_visible_during_session.planets = []
        self.objects_not_defined_during_session.planets = []
        for obj in self.solar_system:
            obj.calculate_rise_and_set()
            if obj.will_be_visible_during_session():
                self.objects_visible_during_session.planets.append(obj)
            else:
                self.objects_not_visible.planets.append(obj)

    def update_now_deepspace_objects(self):
        """ Update current coordinates and other properties for all visible objects """
        self.objects_visible_now.deepspace = []
        self.objects_visible_during_session.deepspace = []
        self.objects_not_visible.deepspace = []
        self.objects_not_defined.deepspace = []
        if self.from_list.deepspace:
            for obj in self.from_list.deepspace:
                try:
                    star_astro = here.at(t).observe(star_obj)
                    star_app = star_astro.apparent()
                    alt, az, d = star_app.altaz('standard')

                    DSOobject = ongc.Dso(obj)
                    ra_arr, dec_arr = DSOobject.getCoords()
                    ra, dec = tuple(ra_arr), tuple(dec_arr)
                    alt_ids = DSOobject.getIdentifiers()
                    messier = alt_ids[0]
                    constellation = DSOobject.getConstellation()
                    obj_type = DSOobject.getType()
                    # TODO …
                except ValueError as e:
                    # print(e)
                    pass
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
