from math import radians, degrees, pi, tan, atan, exp, log

# Convert lon/lat values to 900913 x/y.
A = 6378137
MAXEXTENT = 20037508.342789244


def sm_clamp(x, min, max):
    """Clamps values to within range defined by min, max

    Args:
        x (_type_): _description_
        min (_type_): _description_
        max (_type_): _description_

    Returns:
        _type_: _description_
    """
    x[x < min] = min
    x[x > max] = max
    return x


# https://github.com/mapbox/sphericalmercator/blob/3f61128523aed26904be33463af87a142752a4ad/sphericalmercator.js#L175
def lonlat_to_merc(lon, lat):
    """Transforms coordinates from longitude/latitude to spherical Mercator.

    Args:
        lon (float, decimal): longitude in decimal degrees
        lat (float, decimal): latitude in decimal degrees


    Returns:
        tuple: coordinates in spherical Mercator
    """
    x = A * radians(lon)
    y = A * log(tan((pi * 0.25) + (0.5 * radians(lat))))

    # if xy value is beyond maxextent (e.g. poles), return maxextent.
    x = sm_clamp(x, -MAXEXTENT, MAXEXTENT)
    y = sm_clamp(y, -MAXEXTENT, MAXEXTENT)
    return x, y


def merc_to_lonlat(x, y):
    """Transforms coordinates from spherical Mercator to longitude/latitude.

    Args:
        x (float, decimal): x coordinate
        y (float, decimal): y coordinate

    Returns:
        tuple: coordinates as longitude/latitude.
    """
    return degrees(x / A), degrees(((pi * 0.5) - 2.0 * atan(exp(-y / A))))


def within_merc_extent(x, y):
    """Are points in meters within Mercator extent?

    When doing maths with Mercator coordinates in m, you can end up outside the
    Mercator extent with an undefined coordinate. This function returns true if
    all xy lie within the Mercator extent.

    Args:
        x (float, decimal): x coordinate
        y (float, decimal): y coordinate

    Returns:
        bool
    """
    return all([x, y] <= MAXEXTENT) & all([x, y] >= -MAXEXTENT)


def merc_truncate(x, y):
    """Truncate coordinate to Mercator extent.

    If a point in m lies outside the Mercator extent, this function can be used
    to truncate it to the boundary of the extent.

    Args:
        x (float, decimal): x coordinate
        y (float, decimal): y coordinate

    Returns:
        tuple: a tuple (x,y) of spherical Mercator coordinates.
    """
    return sm_clamp(x, -MAXEXTENT, MAXEXTENT), sm_clamp(y, -
                                                        MAXEXTENT, MAXEXTENT)
