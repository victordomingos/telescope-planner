#!/usr/bin/env python3

from abc import ABC, abstractmethod

from telescope_planner.geocode import get_location, DEFAULT_LOCATION

# Skipping Earth, since we are not planning to support observatories from other planets
SOLAR_SYSTEM = [
    'sun', 'mercury', 'venus', 'moon', 'mars', 'JUPITER BARYCENTER',
    'URANUS BARYCENTER', 'NEPTUNE BARYCENTER', 'PLUTO BARYCENTER'
]


class SpaceObserver(ABC):
    def __init__(self, object_name: str, latitude: float = DEFAULT_LOCATION.latitude,
                 longitude: float = DEFAULT_LOCATION.longitude):
        self.object_name = object_name

        self.ra = None
        self.dec = None
        self.alt = None
        self.az = None
        self.latitude = latitude
        self.longitude = longitude
        self.description: str = ''
        self.names = [object_name]
        self.magnitudes = {'V': None,
                           'B': None,
                           }
        self.is_bookmarked = False
        self.score = 0
        self.kind = ''

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
        return f'<{self.__class__.__name__}: {self.name}, {self.kind} observed from {self.latitude} {self.longitude}>'

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.name}, {self.kind} observed from {self.latitude} {self.longitude}>'


class PlanetObserver(SpaceObserver):
    def __init__(self, object_name, latitude, longitude):
        super().__init__(object_name, latitude, longitude)
        self.kind = 'Solar System object'  # TODO: distinguish between regular planets, dwarf, moons...

    def is_up(self):
        pass

    def update_altaz(self):
        pass

    def update_description(self):
        pass


class DeepSpaceObserver(SpaceObserver):
    def __init__(self, object_name, latitude, longitude):
        super().__init__(object_name, latitude, longitude)
        self.kind = 'Deep Space object'  # TODO: distinguish between stars, galaxies...
        self.constellation = ''

    def is_up(self):
        pass

    def update_altaz(self):
        pass

    def update_description(self):
        pass
