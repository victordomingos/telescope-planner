from types import SimpleNamespace

ONGC_TYPES_NAMES_FROM_ABREVS = {
    '*': 'Star',
    '**': 'Double star',
    '* Ass': 'Association of stars',
    'OCl': 'Open Cluster',
    'GCl': 'Globular Cluster',
    'Cl + N': 'Star cluster + Nebula',
    'G': 'Galaxy',
    'GPair': 'Galaxy Pair',
    'GTrpl': 'Galaxy Triplet',
    'GGroup': 'Group of galaxies',
    'PN': 'Planetary Nebula',
    'HII': 'HII Ionized region',
    'DrkN': 'Dark Nebula',
    'EmN': 'Emission Nebula',
    'Neb': 'Nebula',
    'RfN': 'Reflection Nebula',
    'SNR': 'Supernova remnant',
    'Nova': 'Nova star',
    'NonEx': 'Nonexistent object',
    'Dup': 'Duplicated object',
    'Other': 'Other classification',
}

ONGC_TYPES_ABREVS_FROM_NAMES = {v: k for k, v in ONGC_TYPES_NAMES_FROM_ABREVS.items()}

ONGC_CATALOGS_NAMES_FROM_ABREVS = {
    'NGC': 'NGC',
    'IC': 'IC',
    'M': 'Messier',
}

ONGC_CATALOGS_ABREVS_FROM_NAMES = {v: k for k, v in ONGC_CATALOGS_NAMES_FROM_ABREVS.items()}

# Skipping Earth, since we are not planning to support observatories from other planets
SOLAR_SYSTEM = [
    'sun', 'mercury', 'venus', 'moon', 'mars', 'JUPITER BARYCENTER',
    'URANUS BARYCENTER', 'SATURN BARYCENTER', 'NEPTUNE BARYCENTER',
    'PLUTO BARYCENTER']

OUR_TOP_LIST_PLANETS = ['mercury', 'venus', 'moon', 'mars',
                        'JUPITER BARYCENTER', 'URANUS BARYCENTER',
                        'NEPTUNE BARYCENTER', ]

MESSIER_LIST = ['M' + str(i) for i in range(1, 111)]

# TODO: See if we can add Pleiades here.
OUR_TOP_LIST_DEEPSPACE = [
    'NGC104', 'NGC224', 'NGC253', 'NGC598', 'NGC869', 'NGC884', 'NGC1976',
    'NGC2070', 'NGC3293', 'NGC3372', 'NGC4594', 'NGC5128', 'NGC5139',
    'NGC5236', 'NGC6121', 'NGC6205', 'NGC6405', 'NGC6514', 'NGC6533',
    'NGC6611', 'NGC6618', 'NGC6656', 'NGC6720', 'NGC6853']

CONSTELLATIONS_LATIN_FROM_ABREV = {
    'And': 'Andromeda',
    'Ant': 'Antlia',
    'Aps': 'Apus',
    'Aqr': 'Aquarius',
    'Aql': 'Aquila',
    'Ara': 'Ara',
    'Ari': 'Aries',
    'Aur': 'Auriga',
    'Boo': 'Boötes',
    'Cae': 'Caelum',
    'Cam': 'Camelopardalis',
    'Cnc': 'Cancer',
    'CVn': 'Canes Venatici',
    'CMa': 'Canis Major',
    'CMi': 'Canis Minor',
    'Cap': 'Capricornus',
    'Car': 'Carina',
    'Cas': 'Cassiopeia',
    'Cen': 'Centaurus',
    'Cep': 'Cepheus',
    'Cet': 'Cetus',
    'Cha': 'Chamaeleon',
    'Cir': 'Circinus',
    'Col': 'Columba',
    'Com': 'Coma Berenices',
    'CrA': 'Corona Austrina',
    'CrB': 'Corona Borealis',
    'Crv': 'Corvus',
    'Crt': 'Crater',
    'Cru': 'Crux',
    'Cyg': 'Cygnus',
    'Del': 'Delphinus',
    'Dor': 'Dorado',
    'Dra': 'Draco',
    'Equ': 'Equuleus',
    'Eri': 'Eridanus',
    'For': 'Fornax',
    'Gem': 'Gemini',
    'Gru': 'Grus',
    'Her': 'Hercules',
    'Hor': 'Horologium',
    'Hya': 'Hydra',
    'Hyi': 'Hydrus',
    'Ind': 'Indus',
    'Lac': 'Lacerta',
    'Leo': 'Leo',
    'LMi': 'Leo Minor',
    'Lep': 'Lepus',
    'Lib': 'Libra',
    'Lup': 'Lupus',
    'Lyn': 'Lynx',
    'Lyr': 'Lyra',
    'Men': 'Mensa',
    'Mic': 'Microscopium',
    'Mon': 'Monoceros',
    'Mus': 'Musca',
    'Nor': 'Norma',
    'Oct': 'Octans',
    'Oph': 'Ophiuchus',
    'Ori': 'Orion',
    'Pav': 'Pavo',
    'Peg': 'Pegasus',
    'Per': 'Perseus',
    'Phe': 'Phoenix',
    'Pic': 'Pictor',
    'Psc': 'Pisces',
    'PsA': 'Piscis Austrinus',
    'Pup': 'Puppis',
    'Pyx': 'Pyxis',
    'Ret': 'Reticulum',
    'Sge': 'Sagitta',
    'Sgr': 'Sagittarius',
    'Sco': 'Scorpius',
    'Scl': 'Sculptor',
    'Sct': 'Scutum',
    'Ser': 'Serpens',
    'Sex': 'Sextans',
    'Tau': 'Taurus',
    'Tel': 'Telescopium',
    'Tri': 'Triangulum',
    'TrA': 'Triangulum Australe',
    'Tuc': 'Tucana',
    'UMa': 'Ursa Major',
    'UMi': 'Ursa Minor',
    'Vel': 'Vela',
    'Vir': 'Virgo',
    'Vol': 'Volans',
    'Vul': 'Vulpecula',
}

CONSTELLATIONS_ABREV_FROM_LATIN = {v: k for k, v in CONSTELLATIONS_LATIN_FROM_ABREV.items()}

# Used by default, when there are no location services available
DEFAULT_LOCATION = SimpleNamespace(**{
    'latitude': 41.55926513671875,
    'longitude': -8.405625509894655,
    'altitude': 190.0,
    'city': 'Braga',
    'country': 'Portugal',
    'dms_latitude': '41°33\'33.38\" N',
    'dms_longitude': '8°24\'20.5\" W',
})

# A few alternative locations, for testing purposes:
ALTERNATIVE_LOCATION1 = SimpleNamespace(**{
    'latitude': 51.1739726374,
    'longitude': -1.82237671048,
    'altitude': 92.0,
    'city': 'Stonehenge',
    'country': 'United Kingdom',
    'dms_latitude': '51°10\'26.30" N',
    'dms_longitude': '-1°49\'20.56" W',
})

ALTERNATIVE_LOCATION2 = SimpleNamespace(**{
    'latitude': 28.304474,
    'longitude': -16.509514,
    'altitude': 2390.0,
    'city': 'Izaña, Teide Observatory',
    'country': 'Tenerife, Spain',
    'dms_latitude': '28°18\'00" N',
    'dms_longitude': '16°30\'35" W',
})

ALTERNATIVE_LOCATION3 = SimpleNamespace(**{
    'latitude': -43.9866667,
    'longitude': 170.4650000,
    'altitude': 1027.0,
    'city': 'Mackenzie Basin, Mt. John Observatory',
    'country': 'New Zealand',
    'dms_latitude': '43°59\'12.0"S',
    'dms_longitude': '170°27\'54.0"E',
})
