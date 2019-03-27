#!/usr/bin/env python3

from abc import ABC, abstractmethod

from .geocode import get_location, DEFAULT_LOCATION


class SpaceObserver(ABC):
    def __init__(self):
        self.ra = None
        self.dec = None
        self.alt = None
        self.az = None
        self.latitude: float = DEFAULT_LOCATION.latitude
        self.longitude: float = DEFAULT_LOCATION.longitude
        self.description: str = ''
        self.names = []
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


class PlanetObserver(SpaceObserver):
    def __init__(self):
        super().__init__(self, *args, **kwargs)
        self.kind = 'Planet'  # TODO: distinguish between regular planets, dwarf, moons...

    def is_up(self):
        pass

    def update_altaz(self):
        pass

    def update_description(self):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass


class DeepSpaceObserver(SpaceObserver):
    def __init__(self):
        super().__init__(self, *args, **kwargs)
        self.constellation = ''

    def is_up(self):
        pass

    def update_altaz(self):
        pass

    def update_description(self):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass
