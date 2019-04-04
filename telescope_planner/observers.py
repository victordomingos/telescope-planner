#!/usr/bin/env python3

from abc import ABC, abstractmethod
from pyongc import ongc
from skyfield.api import Star

class SpaceObserver(ABC):
    """ This is a base class that represents a generic space object being
    observed from a specific location on Earth at a given date/time.
    """

    def __init__(self, object_name, session):
        self.object_name = object_name
        self.session = session

        self.ra = None
        self.dec = None
        self.alt = None
        self.az = None
        self.distance = None
        self.user_location = (session.latitude, session.longitude, session.altitude)
        self.description: str = ''
        self.names = [object_name]
        self.magnitudes = {'V': None,
                           'B': None,
                           }
        self.is_bookmarked = False
        self.score = 0
        self.kind = ''
        self.time = session.start
        self.session_rises = None
        self.session_sets = None

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def update_coords(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def is_up_now(self):
        pass

    def will_be_up_during_session(self):
        """Will this object be above the horizon between start and end times?"""
        if self.session_rises or self.session_sets:
            return True
        else:
            return False

    def __str__(self):
        cls_name = self.__class__.__name__
        return f'<{cls_name}: {self.name}, {self.kind} observed from {self.session.latitude} {self.session.longitude}>'

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f'<{cls_name}: {self.name}, {self.kind} observed from {self.session.latitude} {self.session.longitude}>'


class PlanetObserver(SpaceObserver):
    """ This class represents a Solar System object being
    observed from a specific location on Earth at a given date/time.
    """

    def __init__(self, object_name, session):
        super().__init__(object_name, session)
        self.kind = 'Solar System object'  # TODO: distinguish between regular planets, dwarf, moons...

        self.p = session.planets[object_name]
        self.planet_astro_session = self.session.here.at(self.session.start).observe(self.p)
        self.planet_app_session = self.planet_astro_session.apparent()
        self.planet_astro_now = None
        self.planet_app_now = None
        self._name = object_name.split()[0].upper()
        self.update_coords()
        self.calculate_rise_and_set()

    @property
    def name(self):
        return self._name

    def calculate_rise_and_set(self):
        """Estimate date/times for object rises and sets during the session.
        The generated values are made available as lists of dates, as the user
        may eventually try to plan a mega-session spanning more than one night/day.
        """
        # TODO
        self.session_rises = []
        self.session_sets = []

    def will_be_visible_during_session(self):
        """Will this object be above the horizon between start and end times?"""
        # TODO: add other criteria (sun, moon, weather?…)
        return self.will_be_up_during_session()

    def update_coords(self):
        self.planet_astro_now = self.session.here.at(self.session.ts.now()).observe(self.p)
        self.planet_app_now = self.planet_astro_now.apparent()
        self.alt, self.az, self.distance = self.planet_app_now.altaz('standard')

    def is_up_now(self):
        """Is this object above the horizon right now?"""
        if self.alt.degrees > 0.0:
            return True
        else:
            return False

    def get_description(self):
        pass

    @property
    def constellation(self):
        return ''  # TODO: estimate which constellation where this planet may be at.


class DeepSpaceObserver(SpaceObserver):
    """ This class represents a Deep Space object (star, galaxy, nebula,…)
    being observed from a specific location on Earth at a given date/time.
    """

    def __init__(self, object_name, session):
        super().__init__(object_name, session)
        if type(object_name) == ongc.Dso:
            self.dso = object_name  # If class initialized directly with a Dso, use it, else create a new one.
        else:
            try:
                self.dso = ongc.Dso(object_name)
            except Exception as e:
                print(e)
        #print("DSO:", self.dso, type(self.dso))

        #self.kind = 'Deep Space object'  # TODO: distinguish between stars, galaxies...
        #self.constellation = ''
        ra_arr, dec_arr = self.dso.getCoords()
        self.ra, self.dec = tuple(ra_arr), tuple(dec_arr)
        self.alt_ids = self.dso.getIdentifiers()
        self.constellation = self.dso.getConstellation()
        self.kind = self.dso.getType()
        self.star = Star(ra_hours=self.ra, dec_degrees=self.dec)
        self.star_astro_now = self.astrometric = self.session.here.at(self.session.start).observe(self.star)
        self.apparent = self.astrometric.apparent()

        self.alt, self.az, self.distance = self.apparent.altaz('standard')

        ra_arr, dec_arr = self.dso.getCoords()
        self.ra, self.dec = tuple(ra_arr), tuple(dec_arr)
        self.alt_ids = self.dso.getIdentifiers()
        self.messier = self.alt_ids[0]
        self.constellation = self.dso.getConstellation()
        self.kind = self.dso.getType()

    @property
    def name(self):
        return self.dso.getName()

    def update_coords(self):
        pass

    def get_description(self):
        pass

    def is_up_now(self):
        """Is this object above the horizon right now?"""
        if self.alt.degrees > 0.0:
            return True
        else:
            return False

    def update_coords(self):
        self.star_astro_now = self.session.here.at(self.session.ts.now()).observe(self.star)
        self.apparent = self.astrometric.apparent()
        self.alt, self.az, self.distance = self.apparent.altaz('standard') # NOTE: distance has no meaningful value here TODO

    def get_description(self):
        pass
