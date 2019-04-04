#!/usr/bin/env python3
import logging

from types import SimpleNamespace

from pyongc.ongc import listObjects
from skyfield.api import Loader, Topos, load, Angle

from telescope_planner.constants import DEFAULT_LOCATION, SOLAR_SYSTEM
from telescope_planner.constants import ONGC_CATALOGS_ABREVS_FROM_NAMES, CONSTELLATIONS_ABBREV_FROM_LATIN
from telescope_planner.constants import ONGC_TYPES_ABREVS_FROM_NAMES
from telescope_planner.geocode import get_location
from telescope_planner.observers import PlanetObserver, DeepSpaceObserver
from telescope_planner.settings import DATA_FOLDER


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_dso_list(catalog=None, kind=None, constellation=None, uptovmag=None, limit=None):
    params = dict()

    if (catalog is not None) and (catalog in ONGC_CATALOGS_ABREVS_FROM_NAMES.keys()):
        params.update({'catalog': ONGC_CATALOGS_ABREVS_FROM_NAMES[catalog]})

    if (kind is not None) and (kind in ONGC_TYPES_ABREVS_FROM_NAMES.keys()):
        params.update({'type': ONGC_TYPES_ABREVS_FROM_NAMES[kind]})

    if (constellation is not None) and (constellation in CONSTELLATIONS_ABBREV_FROM_LATIN.keys()):
        params.update({'constellation': CONSTELLATIONS_ABBREV_FROM_LATIN[constellation]})

    if uptovmag is not None and is_float(uptovmag):
        params.update({'uptovmag': float(uptovmag)})

    return [obj for obj in listObjects(**params)[0:limit]
            if obj.getType() != "Duplicated record"]


def is_inside_window(obj, min_ra, min_dec, max_ra, max_dec):
    #TODO: debug these data types ;-)
    if (min_ra <= obj.getRA() <= max_ra) and (min_dec <= obj.getDec() <= max_dec):
        return True
    else:
        return False

class Session:
    def __init__(self, timescale=None, start=None, end=None, latitude=DEFAULT_LOCATION.latitude,
                 longitude=DEFAULT_LOCATION.longitude, altitude=DEFAULT_LOCATION.altitude, min_alt=0.0, max_alt=90.0,
                 min_az=0.0, max_az=360.0, constellation=None, only_kind=None, min_apparent_mag=None,
                 only_from_catalog=None, only_these_sources=None, limit=None):
        self.start = start if start is not None else get_next_sunset()
        self.end = end if end is not None else get_next_sunrise()

        self.ts = timescale

        # user/observatory location:
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

        # restrict current session to objects that are inside or near a specific constellation:
        self.constellation = constellation

        # Kind
        self.only_kind = only_kind if only_kind is not None else None
        # restrict current session to objects with apparent magnitude greater than:
        self.min_apparent_mag = min_apparent_mag

        # restrict current session to objects in these catalogs:
        self.using_catalogs = only_from_catalog if only_from_catalog is not None else []
        self.only_these_sources = only_these_sources

        self.limit = limit

        self.objects_visible_now = SimpleNamespace(**{'planets': [], 'deepspace': []})
        self.objects_not_visible = SimpleNamespace(**{'planets': [], 'deepspace': []})
        self.objects_not_defined = SimpleNamespace(**{'planets': [], 'deepspace': []})

        self.objects_visible_during_session = SimpleNamespace(**{'planets': [], 'deepspace': []})
        self.objects_not_visible_during_session = SimpleNamespace(**{'planets': [], 'deepspace': []})
        self.objects_not_defined_during_session = SimpleNamespace(**{'planets': [], 'deepspace': []})

        load = Loader(DATA_FOLDER)
        self.planets = load('de421.bsp')
        self.earth = self.planets['earth']
        self.here = self.earth + Topos(latitude=f'{self.latitude} N',
                                       longitude=f'{self.longitude} E',
                                       elevation_m=self.altitude)

        # Use minimum altitude/azimuth provided for this session (depending for
        # instance on the telescope mount angles or any physical obstacles on
        # the observatory), define a window constraint converting from alt/az to ra/dec,
        # for current location/datetime:
        #ts = load.timescale()
        #planets = load('de421.bsp')
        #earth = planets['earth']

        self.moment = self.ts.now()
        #self.here = earth + Topos(latitude=f'{self.latitude} N',
        #                     longitude=f'{self.longitude} E',
        #                     elevation_m=self.altitude)

        self.min_ra, self.min_dec, _ = self.here.at(self.moment).from_altaz(alt_degrees=min_alt, az_degrees=min_az).radec()
        self.max_ra, self.max_dec, _ = self.here.at(self.moment).from_altaz(alt_degrees=max_alt, az_degrees=max_az).radec()

        self.update_user_location(self.latitude, self.longitude)
        self.deepspace_selection = []

        if self.only_these_sources is not None:
            if self.only_these_sources.planets:
                logging.debug("=== Using our Top List for Solar System")  # DEBUG
                self.solar_system = [PlanetObserver(name, self)
                                     for name in self.only_these_sources.planets]
            else:
                logging.debug("=== Using All Planets from Solar System")  # DEBUG
                self.solar_system = [PlanetObserver(name, self) for name in SOLAR_SYSTEM]

            if self.only_these_sources.deepspace:
                logging.debug("=== Using our Top List for Solar System")  # DEBUG
                for obj_id in self.only_these_sources.deepspace:
                    try:
                        self.deepspace_selection.append(DeepSpaceObserver(obj_id, self))
                    except ValueError as e:
                        logging.warning(e)
            else:
                logging.debug("=== Not using Deep Space this time")  # DEBUG
                self.deepspace_selection = []
        else:
            logging.debug("=== Using our Top List for Solar System")  # DEBUG
            self.solar_system = [PlanetObserver(name, self) for name in SOLAR_SYSTEM]
            logging.debug(f"=== Using session parameters for Deep Space {only_from_catalog} {only_kind} {constellation} {min_apparent_mag} {self.limit}")  # DEBUG
            selection = []
            selection += get_dso_list(catalog=only_from_catalog,
                                      kind=only_kind,
                                      constellation=constellation,
                                      uptovmag=min_apparent_mag,
                                      limit=self.limit,
                                      # TODO: Add min_ra, min_dec, max_ra, max_dec here
                                      )

            selection_filtered = [obj for obj in selection
                                  if is_inside_window(obj, self.min_ra, self.min_dec,self.max_ra, self.max_dec,)]

            for obj in selection:
                try:
                    self.deepspace_selection.append(DeepSpaceObserver(obj, self))
                except Exception as e:
                    logging.warning(e)
            logging.debug("=== Updating current positions for solar system objects")  # DEBUG
            self.update_now_solar_objects()
            logging.debug("=== Updating current positions for deep space objects")  # DEBUG
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

    def get_next_sunset():
        pass

    def get_next_sunrise():
        pass

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

        for obj in self.deepspace_selection:
            try:
                obj.update_coords()
                if obj.is_up_now():
                    self.objects_visible_now.deepspace.append(obj)
                else:
                    self.objects_not_visible.deepspace.append(obj)
            except ValueError as e:
                logging.warning(e)

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f'<{cls_name}: Lat.{self.latitude}, Long.{self.longitude} | {self.start.utc_datetime()}>'

    def __str__(self):
        cls_name = self.__class__.__name__
        return f'<{cls_name}: Lat.{self.latitude}, Long.{self.longitude} | {self.start.utc_datetime()}>'
