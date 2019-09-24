""" transforms involving AER: azimuth, elevation, slant range"""
from typing import Tuple
from datetime import datetime

from .ecef import ecef2enu, geodetic2ecef, ecef2geodetic, enu2uvw
from .enu import geodetic2enu, aer2enu, enu2aer
from .ellipsoid import Ellipsoid

try:
    from .eci import eci2ecef, ecef2eci
except ImportError:
    eci2ecef = ecef2eci = None

__all__ = ["aer2ecef", "ecef2aer", "geodetic2aer", "aer2geodetic", "eci2aer", "aer2eci"]


def ecef2aer(
    x: float, y: float, z: float, lat0: float, lon0: float, h0: float, ell: Ellipsoid = None, deg: bool = True
) -> Tuple[float, float, float]:
    """
    compute azimuth, elevation and slant range from an Observer to a Point with ECEF coordinates.

    ECEF input location is with units of meters

    Parameters
    ----------

    x : float
        ECEF x coordinate (meters)
    y : float
        ECEF y coordinate (meters)
    z : float
        ECEF z coordinate (meters)
    lat0 : float
        Observer geodetic latitude
    lon0 : float
        Observer geodetic longitude
    h0 : float
         observer altitude above geodetic ellipsoid (meters)
    ell : Ellipsoid, optional
        reference ellipsoid
    deg : bool, optional
        degrees input/output  (False: radians in/out)

    Returns
    -------
    az : float
         azimuth to target
    el : float
         elevation to target
    srange : float
         slant range [meters]
    """
    xEast, yNorth, zUp = ecef2enu(x, y, z, lat0, lon0, h0, ell, deg=deg)

    return enu2aer(xEast, yNorth, zUp, deg=deg)


def geodetic2aer(
    lat: float, lon: float, h: float, lat0: float, lon0: float, h0: float, ell: Ellipsoid = None, deg: bool = True
) -> Tuple[float, float, float]:
    """
    gives azimuth, elevation and slant range from an Observer to a Point with geodetic coordinates.


    Parameters
    ----------

    lat : float
        target geodetic latitude
    lon : float
        target geodetic longitude
    h : float
        target altitude above geodetic ellipsoid (meters)
    lat0 : float
        Observer geodetic latitude
    lon0 : float
        Observer geodetic longitude
    h0 : float
         observer altitude above geodetic ellipsoid (meters)
    ell : Ellipsoid, optional
          reference ellipsoid
    deg : bool, optional
          degrees input/output  (False: radians in/out)

    Returns
    -------
    az : float
         azimuth
    el : float
         elevation
    srange : float
         slant range [meters]
    """
    e, n, u = geodetic2enu(lat, lon, h, lat0, lon0, h0, ell, deg=deg)

    return enu2aer(e, n, u, deg=deg)


def aer2geodetic(
    az: float, el: float, srange: float, lat0: float, lon0: float, h0: float, ell: Ellipsoid = None, deg: bool = True
) -> Tuple[float, float, float]:
    """
    gives geodetic coordinates of a point with az, el, range
    from an observer at lat0, lon0, h0

    Parameters
    ----------
    az : float
         azimuth to target
    el : float
         elevation to target
    srange : float
         slant range [meters]
    lat0 : float
           Observer geodetic latitude
    lon0 : float
           Observer geodetic longitude
    h0 : float
         observer altitude above geodetic ellipsoid (meters)
    ell : Ellipsoid, optional
          reference ellipsoid
    deg : bool, optional
          degrees input/output  (False: radians in/out)

    Returns
    -------

    In reference ellipsoid system:

    lat : float
          geodetic latitude
    lon : float
          geodetic longitude
    alt : float
          altitude above ellipsoid  (meters)
    """
    x, y, z = aer2ecef(az, el, srange, lat0, lon0, h0, ell=ell, deg=deg)

    return ecef2geodetic(x, y, z, ell=ell, deg=deg)


def eci2aer(
    x: float, y: float, z: float, lat0: float, lon0: float, h0: float, t: datetime, useastropy: bool = True
) -> Tuple[float, float, float]:
    """
    takes Earth Centered Inertial x,y,z ECI coordinates of point and gives az, el, slant range from Observer

    Parameters
    ----------

    x : float
        ECI x-location [meters]
    y : float
        ECI y-location [meters]
    z : float
        ECI z-location [meters]
    lat0 : float
           Observer geodetic latitude
    lon0 : float
           Observer geodetic longitude
    h0 : float
         observer altitude above geodetic ellipsoid (meters)
    t : datetime.datetime
        Observation time
    useastropy: bool, optional
        Force use / non-use of AstroPy (default use AstroPy if available)

    Returns
    -------
    az : float
         azimuth to target
    el : float
         elevation to target
    srange : float
         slant range [meters]
    """
    if eci2ecef is None:
        raise ImportError("pip install numpy")

    xecef, yecef, zecef = eci2ecef(x, y, z, t, useastropy=useastropy)

    return ecef2aer(xecef, yecef, zecef, lat0, lon0, h0)


def aer2eci(
    az: float,
    el: float,
    srange: float,
    lat0: float,
    lon0: float,
    h0: float,
    t: datetime,
    ell=None,
    deg: bool = True,
    useastropy: bool = True,
) -> Tuple[float, float, float]:
    """
    gives ECI of a point from an observer at az, el, slant range

    Parameters
    ----------
    az : float
         azimuth to target
    el : float
         elevation to target
    srange : float
         slant range [meters]
    lat0 : float
           Observer geodetic latitude
    lon0 : float
           Observer geodetic longitude
    h0 : float
         observer altitude above geodetic ellipsoid (meters)
    t : datetime.datetime
        Observation time
    ell : Ellipsoid, optional
          reference ellipsoid
    deg : bool, optional
          degrees input/output  (False: radians in/out)
    useastropy: bool, optional
        Force use / non-use of AstroPy (default use AstroPy if available)

    Returns
    -------

    Earth Centered Inertial x,y,z

    x : float
        ECEF x coordinate (meters)
    y : float
        ECEF y coordinate (meters)
    z : float
        ECEF z coordinate (meters)
    """
    if ecef2eci is None:
        raise ImportError("pip install numpy")

    x, y, z = aer2ecef(az, el, srange, lat0, lon0, h0, ell, deg)

    return ecef2eci(x, y, z, t, useastropy=useastropy)


def aer2ecef(
    az: float, el: float, srange: float, lat0: float, lon0: float, alt0: float, ell: Ellipsoid = None, deg: bool = True
) -> Tuple[float, float, float]:
    """
    converts target azimuth, elevation, range from observer at lat0,lon0,alt0 to ECEF coordinates.

    Parameters
    ----------
    az : float
         azimuth to target
    el : float
         elevation to target
    srange : float
         slant range [meters]
    lat0 : float
           Observer geodetic latitude
    lon0 : float
           Observer geodetic longitude
    h0 : float
         observer altitude above geodetic ellipsoid (meters)
    ell : Ellipsoid, optional
          reference ellipsoid
    deg : bool, optional
          degrees input/output  (False: radians in/out)

    Returns
    -------

    ECEF (Earth centered, Earth fixed)  x,y,z

    x : float
        ECEF x coordinate (meters)
    y : float
        ECEF y coordinate (meters)
    z : float
        ECEF z coordinate (meters)


    Notes
    ------
    if srange==NaN, z=NaN
    """
    # Origin of the local system in geocentric coordinates.
    x0, y0, z0 = geodetic2ecef(lat0, lon0, alt0, ell, deg=deg)
    # Convert Local Spherical AER to ENU
    e1, n1, u1 = aer2enu(az, el, srange, deg=deg)
    # Rotating ENU to ECEF
    dx, dy, dz = enu2uvw(e1, n1, u1, lat0, lon0, deg=deg)
    # Origin + offset from origin equals position in ECEF
    return x0 + dx, y0 + dy, z0 + dz
