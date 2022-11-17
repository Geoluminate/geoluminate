from math import radians, degrees, asinh, pi, tan, floor, atan, sinh
from .mercator import sm_clamp

WEB_MERCATOR_CRS = dict(
    epsg=3857,
    proj4string="+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs",
)

LONLAT_CRS = dict(
    epsg=4326,
    proj4string="+proj=longlat +datum=WGS84 +no_defs"
)


def lonlat_to_tilenum(lon_deg, lat_deg, zoom):
    """Convert longitude and latitude to slippy tile numbers.

        Returns the Open Street Map slippy map tile numbers (x, y) the
        supplied latitude and longitude fall on, for a given zoom level.

        The point specified by lon_deg` and `lat_deg` is assumed to be in ESPG:4326
        coordinate reference system.

    Args:
        lon_deg (float, decimal): degrees longitude for point
        lat_deg (float, decimal): degrees latitude for point
        zoom (int): zoom level for tile calculation. Increasing zoom increases the number of tiles.

    Returns:
        tuple: x_tile number and y_tile number (x, y)
    """

    # Implementing slippy map spec as per
    # https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames

    x = (1 + (radians(lon_deg) / pi)) / 2
    y = (1 - (asinh(tan(radians(lat_deg))) / pi)) / 2

    n_tiles = 2 ** zoom

    # The values are clamped to prevent problems at the extent boundaries. Eg 180
    # degrees lon which would lon_rad of pi.
    xtile = sm_clamp(floor(x * n_tiles), 0, n_tiles - 1)
    ytile = sm_clamp(floor(y * n_tiles), 0, n_tiles - 1)

    return xtile, ytile


def tilenum_to_lonlat(x, y, zoom):
    """Convert slippy map tiles numbers to latitude and longitude

    Returns the latitude and longitude of the top left corner of a slippy map tile
    specified by `x`, `y` for a given zoom level.

    Args:
        x (int): slippy map tile number in x domain (left to right)
        y (int): slippy map tile number in y domain (top to bottom)
        zoom (int): the zoom level for the calculation. Increasing zoom increases the number of tiles.

    Returns:
        tuple: longitude and latitude (long, lat)
    """
    n_tiles = 2 ** zoom

    lon_rad = (((x / n_tiles) * 2) - 1) * pi

    merc_lat = (1 - ((y / n_tiles) * 2)) * pi
    lat_rad = atan(sinh(merc_lat))

    return degrees(lon_rad), degrees(lat_rad)


def bbox_to_tile_grid(bbox, zoom=None, max_tiles=None):
    """Calculate a slippy map tile grid that will fit a supplied bounding box.

        The grid is returned as part of a tile_grid object that contains a
        data.frame of x,y tile numbers and zoom level.

        The tile grid can be calculated for a given zoom level or for the
        deepest zoom that ensures the number of tiles is less than or equal
        to `max_tiles`.

        If `zoom` and `max_tiles` are supplied together, then the max is still
        enforced and the function will fail if more tiles are required for the
        given zoom.

    Args:
        bbox (list, tuple): the bounding box to fit onto a grid of tiles.
        [xmin,xmax,ymin,ymax].
        zoom (int, optional): The desired zoom level. Defaults to None.
        max_tiles (int, optional): The maximum number of tiles the grid may
        occupy. Defaults to None.

    Returns:
        dict: a dictionary containing 'tiles' and 'zoom'.

    Example:
        >>> bbox = dict(xmin = 152.938485,
                        ymin = -26.93345,
                        xmax = 152.956467,
                        ymax = -26.921463)

        # Get a grid of the minimum number of tiles for a given zoom
        >>> bbox_to_tile_grid(bbox, zoom=15)

        # Get a grid of at most 12 tiles, choosing the most detailed zoom
        # possible.
        >>> bbox_to_tile_grid(bbox, max_tiles=12)

    """

    if zoom is None and max_tiles is None:
        stop("at least one of the zoom or max_tiles arugments must be supplied")

    # No zoom, we'll do a query and choose the best zoom for the max_tiles
    # budget
    if (purrr:: is_null(zoom)){
        tile_query = bbox_tile_query(bbox, zoom_levels=0: 19)
        suitable_zooms = tile_query$total_tiles <= max_tiles
        zoom = tile_query$zoom[max(which(suitable_zooms))]
    }

    tile_extent = bbox_tile_extent(bbox, zoom)

    x_tiles = tile_extent$x_min: tile_extent$x_max
    y_tiles = tile_extent$y_min: tile_extent$y_max

    if(!purrr: : is_null(max_tiles) & & (length(x_tiles) * length(y_tiles)) > max_tiles){
        stop("Bounding box needed more than max_tiles at specified zoom level. Check with bbox_tile_query(bbox)")
    }

    return {
        "tiles": expand.grid(x=x_tiles, y=y_tiles),
        "zoom": zoom
    }


def bbox_tile_query(bbox, zoom_levels=2: 18):
    """Bounding box tile query

    Determines how many tiles the bounding box would occupy for a range of zooms.
    Useful for working out what is a reasonable zoom to work at. Each tile is a separate
    request from the server.

    Tiles are typically 256x256 pixels and are tens of Kb in size, you can get some sense
    of the data from the query also.

    Args:
        bbox (_type_): _description_
        zoom_levels (_type_, optional): _description_. Defaults to 2:18.

    Returns:
        dataframe: a data frame containing tile usage information for the bounding box
   at each zoom level.
    """

    extents_at_zooms = purrr:: map(zoom_levels,
                                    ~bbox_tile_extent(bbox, .))

    extents_at_zooms = lol_to_df(extents_at_zooms)

    extents_at_zooms$y_dim =
    abs(extents_at_zooms$y_max - extents_at_zooms$y_min) + 1
    extents_at_zooms$x_dim =
    abs(extents_at_zooms$x_max - extents_at_zooms$x_min) + 1
    extents_at_zooms$total_tiles =
    extents_at_zooms$y_dim * extents_at_zooms$x_dim
    extents_at_zooms$zoom = zoom_levels

    return extents_at_zooms


def bbox_tile_extent(bbox, zoom):
    """Convert a bounding box from latitude and longitude to tile numbers

    This function creates an analog of a bounding box but in tile numbers. It
    returns the min and max x and y tile numbers for a tile grid that would fit
    the bounding box for a given zoom level.

    Args:
        bbox (_type_): a bbox object created by `sf::st_bbox`, or a vector with names
   'xmin', 'xmax', 'ymin', 'ymax'
        zoom (_type_): zoom level to calculate the tile grid on.

    Returns:
        dict: a dict containing keys `x_min`, `y_min`, `x_max`, `y_max`
    """

    min_tile = lonlat_to_tilenum(lat_deg=bbox["ymin"],
                                 lon_deg=bbox["xmin"], zoom)
    max_tile = lonlat_to_tilenum(lat_deg=bbox["ymax"],
                                 lon_deg=bbox["xmax"], zoom)

    return dict(x_min=min_tile$x,
                y_min=max_tile$y,
                x_max=max_tile$x,
                y_max=min_tile$y)

    # Note tile numbers start at 0 in the north and increase going south. The
    # have the opposite polarity to latitude which increases going north. This is
    # why y_min = max_tile$y here.


def tile_bbox(x, y, zoom):
    """Calculate the bounding box for a tile in latitude and longitude

    Given a slippy maps tile specified by `x`, `y`, and `zoom`, return the
    an `sf` bounding box object for the tile with units in metres using the
    EPSG:3857 coordinate reference system (Web Mercator).

    Args:
        x (int): slippy map tile x number
        y (int): slippy map tile y number
        zoom (int): zoom level for tile

    Returns:
        an sf bbox object.
    """
    bottom_left =
    lonlat_to_merc(t(as .matrix(unlist(tilenum_to_lonlat(x, y + 1, zoom)))))

    top_right =
    lonlat_to_merc(t(as .matrix(unlist(tilenum_to_lonlat(x + 1, y, zoom)))))

    return structure(c(xmin=bottom_left[[1]],
                       ymin=bottom_left[[2]],
                       xmax=top_right[[1]],
                       ymax=top_right[[2]]),
                     class = "bbox",
                     crs=.global_sm_env$WEB_MERCATOR_CRS)


def tile_grid_bboxes(tile_grid):
    """Get tile grid bounding boxes

    Given an tile_grid object like that returned from `bbox_to_tile_grid`, return
    a list of sf style bounding box objects, one for each tile in the grid, in the same order
    as tiles in `tile_grid$tiles`.

    The bounding box units are metres in the EPSG:3857 coordinate reference
    system (Web Mercator).

    Args:
        tile_grid (dict): a tile_grid dict as returned from `bbox_to_tile_grid`

    Returns:
        _type_: _description_
    """
    if (!is_tile_grid(tile_grid)) stop("tile_grid must be of class tile_grid - output from bbox_to_tile_grid()")

    purrr:: pmap(.l = tile_grid$tiles,
                  .f= tile_bbox,
                  zoom= tile_grid$zoom)
    return []


def compose_tile_grid(tile_grid, images):
    """Compose a list of images using tile_grid data.

    Given a tile_grid object and a list of images, compose the images into a
    single spatially referenced RasterBrick object.

    The list of images is assumed to be in corresponding order to the tiles in
    the tile_grid object.

    The returned object uses the Web Mercator projection, EPSG:3857, which is
    the native crs of the tiles.

    Args:
        tile_grid (_type_): a tile_grid object, likely returned from `bbox_to_tile_grid`
        images (_type_): a list of character strings defining paths to images. Matched to tiles in tile_grid based on list position.

    Returns:
        a spatially reference raster
    """
    bricks =
        purrr:: pmap(.l = list(x = tile_grid$tiles$x,
                                y= tile_grid$tiles$y,
                                image= images),
                      .f= function(x, y, image, zoom){
            bbox=tile_bbox(x, y, zoom)
            raster_img=            raster: : brick(image,
                                                  crs= attr(bbox, "crs")$proj4string)
            raster:: extent(raster_img) =
            raster: : extent(bbox[c("xmin", "xmax", "ymin", "ymax")])
            raster_img
        },
            zoom=tile_grid$zoom)

    geo_refd_raster = do.call(raster: : merge, bricks)

    return geo_refd_raster
