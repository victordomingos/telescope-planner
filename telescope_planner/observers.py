#!/usr/bin/env python3

from abc import ABC, abstractmethod

from telescope_planner.geocode import get_location
from telescope_planner.constants import DEFAULT_LOCATION, NOW


class SpaceObserver(ABC):
    """ This is a base class that represents a generic space object being
    observed from a specific location on Earth at a given date/time.
    """

    def __init__(self, object_name, location, time=NOW):
        self.object_name = object_name

        self.ra = None
        self.dec = None
        self.alt = None
        self.az = None
        self.distance = None
        self.user_location = location
        #self.latitude = latitude
        #self.longitude = longitude
        self.description: str = ''
        self.names = [object_name]
        self.magnitudes = {'V': None,
                           'B': None,
                           }
        self.is_bookmarked = False
        self.score = 0
        self.kind = ''
        self.time = time

    @property
    def name(self):
        return self.names[0]

    def check_user_location(self):
        location, source = get_location()
        self.update_user_location(location.latitude, location.longitude)

    def update_user_location(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude
        # TODO: update anything that depends on the user location

    @abstractmethod
    def update_altaz(self):
        pass

    @abstractmethod
    def update_description(self):
        pass

    @abstractmethod
    def is_up(self):
        pass

    def __str__(self):
        cls_name = self.__class__.__name__
        return f'<{cls_name}: {self.name}, {self.kind} observed from {self.latitude} {self.longitude}>'

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f'<{cls_name}: {self.name}, {self.kind} observed from {self.latitude} {self.longitude}>'


class PlanetObserver(SpaceObserver):
    """ This class represents a Solar System object being
    observed from a specific location on Earth at a given date/time.
    """
    def __init__(self, object_name, location, time):
        super().__init__(object, location, time)
        self.kind = 'Solar System object'  # TODO: distinguish between regular planets, dwarf, moons...
        self.here = here
        self.p = planets[object_name]
        self.planet_astro = self.here.at(t).observe(p)
        self.planet_app = self.planet_astro.apparent()
        self.name = planet.split()[0].upper()
        self.update_altaz()
        self.is_up()

    def is_up(self):
        if self.alt.degrees > 0.0:
            return True
        else:
            return False
        
    def update_altaz(self):
        self.alt, self.az, self.distance = planet_app.altaz('standard')

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

    def update_altaz(self):
        pass

    def update_description(self):
        pass
