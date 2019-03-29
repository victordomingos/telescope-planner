#!/usr/bin/env python3

from abc import ABC, abstractmethod


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

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def update_altaz(self):
        pass

    @abstractmethod
    def update_description(self):
        pass

    @abstractmethod
    def is_up(self):
        pass

    @abstractmethod
    def will_be_up(self):
        pass

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
        self.planet_astro = self.session.here.at(self.session.start).observe(self.p)
        self.planet_app = self.planet_astro.apparent()
        self._name = object_name.split()[0].upper()
        self.update_altaz()
        self.is_up()

    @property
    def name(self):
        return self._name

    def is_up(self):
        """Will this object above the horizon at the observation start time?"""
        if self.alt.degrees > 0.0:
            return True
        else:
            return False

    def will_be_up(self):
        """Will this object be above the horizon between start and end times?"""
        #self.planet_astro_interval = self.session.here.at(self.session.start).observe(self.p)
        #self.planet_app_interval = self.planet_astro_interval.apparent()
        pass # TODO

    def update_altaz(self):
        self.alt, self.az, self.distance = self.planet_app.altaz('standard')

    def update_description(self):
        pass

    @property
    def constellation(self):
        return ''  # TODO: estimate which constellation where this planet may be at.


class DeepSpaceObserver(SpaceObserver):
    """ This class represents a Deep Space object (star, galaxy, nebula,…)
    being observed from a specific location on Earth at a given date/time.
    """
    def __init__(self, object_name, latitude, longitude, time):
        super().__init__(object_name, latitude, longitude, time)
        self.kind = 'Deep Space object'  # TODO: distinguish between stars, galaxies...
        self.constellation = ''

    def is_up(self):
        pass

    def will_be_up(self):
        """Will this object be above the horizon between start and end times?"""
        pass

    def update_altaz(self):
        pass

    def update_description(self):
        pass
