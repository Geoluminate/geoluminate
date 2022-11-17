from math import radians, degrees


def raster_to_png(tile_raster, file_path):
    """Write a raster to PNG

    Args:
        tile_raster (_type_): the raster to write to PNG
        file_path (_type_): the path to write the raster
    """

    # png expects 0-1 values, so normalise:
    normalised_raster = normalise_raster(tile_raster)

    #   png::writePNG(normalised_raster, target = file_path)


def normalise_raster(a_raster):
    sweep(raster:: as.array(a_raster),
          MARGIN=3,
          STATS=a_raster @ data @ max,
          FUN="/")


def lol_to_df(lol):
    lov < - purrr: : map(purrr: : transpose(lol), unlist)
    purrr:: lift_dl(data.frame)(lov)
