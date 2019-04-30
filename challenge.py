import time

from astroplan import Observer, is_observable, AirmassConstraint, FixedTarget
from astropy.coordinates import EarthLocation, SkyCoord
from astropy.time import Time
from astropy.io import ascii
from astropy import units as u


# List of dictionaries containing observatory info
# Specific observatory format; may need to prepare more general function to
# deal with other formatas

observatories = [
    {'name': "EABA",
     'location': EarthLocation.from_geodetic(lon='-64.5467d',
                                             lat='-31.5983d',
                                             height=1350 * u.m)},
    {'name': "Macon",
     'location': EarthLocation.from_geodetic(lon='-67.2995d',
                                             lat='-24.5554d',
                                             height=4600 * u.m)},
    {'name': "Mamalluca",
     'location': EarthLocation.from_geodetic(lon='-70.6833d',
                                             lat='-29.9833d',
                                             height=1100 * u.m)},
    {'name': "CTMO",
     'location': EarthLocation.from_geodetic(lon='-97.568956d',
                                             lat='25.995789d',
                                             height=12 * u.m)},
    {'name': "Guillermo Haro",
     'location': EarthLocation.from_geodetic(lon='-110.384722d',
                                             lat='31.052778d',
                                             height=2480 * u.m)},
]


# Table containing Name, RA (in hour angle!!) and Dec (in degrees)
# Specific target list format; may need to prepare more general function to
# deal with other formats

target_list = ascii.read("""
PGC003183   0.90109 73.08478
UGC03858    7.51289 73.63019
UGC03859    7.51347 73.70633
UGC03889    7.56557 73.64353
PGC616899   14.55716    -37.83552
PGC021381   7.61031 74.44653
PGC021386   7.61209 74.45029
UGC03929    7.66532 75.42469
ESO336-006  18.60201    -37.94586
ESO336-001  18.54346    -39.45677
ESO327-012  14.71358    -40.60005
UGC11902    22.09344    16.72152
UGC02860    3.85436 78.29756
UGC11848    21.92643    10.46645
ESO328-031  15.20782    -42.01764
PGC3082596  15.25485    -40.80312
PGC069732   22.79608    40.12161
PGC2211350  22.99214    43.02606
NGC7379 22.79249    40.23881
ESO274-008  15.29708    -43.50163
""")


# Complete with Apr 10, 2019 and chosen time here
date_time = Time("2019-04-10 06:00", "2019-04-10 10:00")


def filter_targets(obs, i, target_list, date_time, roof=2.5):
    """

    A function that filters a list of targets and returns a list with airmass
    less than < 2.5.

    TO IMPLEMENT:
        Move the testing to a different file or into a different function

    Args:
        obs: List of Observer objects that represent observatories
        target_list: List of FixedTarget objects that represent target coords
        date_time: The date and time range over which we check for
            observability
        roof: Float defining the maximum airmass we'll allow for our targets;
            will exclude targets with airmass larger than 2.5

    Returns:
        None

    """
    targets = format_targets(target_list)
    observers = format_observatories(obs)
    airmass_max = AirmassConstraint(roof)
    observability = is_observable(airmass_max, observers[i], targets,
                                  date_time)
    print(observability)
    print("Success!!")


def format_observatories(observatories):
    """

    A function that takes an input containing observatory information and
    formally casts it into a list of Observer objects.

    TO IMPLEMENT:
        Only takes a list of dictionaries as input, consider generalizing -
            IMPLEMENTED, BUT COULD BE BETTER

    Args:
        observatories: List of dictionaries, with each dictionary containing
            the information necessary to initialize an Observer object

                {'name' key : string value,
                 'location' key : EarthLocation value}

    Returns:
        List of Observer objects

    """
    if type(observatories) is list:
        return [Observer(location=observatory.get('location'),
                         name=observatory.get('name'))
                for observatory in observatories]

    elif type(observatories) is dict:
        return Observer(location=observatories.get('location'),
                        name=observatories.get('name'))


def format_targets(targets):
    """

    A function that takes an input containing target information and formally
    casts it into a list of FixedTarget objects.

    TO IMPLEMENT:
        Only takes a table with rows representing targets as input, consider
            generalizing

    Args:
        targets: Table with rows that pertain to individual targets, formatted
            Name as string, RA as hour angle, and Dec as degree

    Returns:
        List of FixedTarget objects, one per row in the table

    """
    return [FixedTarget(SkyCoord(ra=target[1]*u.hour, dec=target[2]*u.deg),
                        name=target[0])
            for target in targets]


start = time.time()
filter_targets(observatories, 3, target_list, date_time)
end = time.time()
print(end - start)
