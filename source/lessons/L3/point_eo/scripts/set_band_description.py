"""
Set Band descriptions
Usage:
    python set_band_desc.py raster bands
Where:
    raster = raster filename
    bands = file containing band names in order
Example:
    python set_band_desc.py raster.tif bandnames.txt

"""
import sys
from osgeo import gdal


def set_band_descriptions(filepath, bands):
    """
    filepath: path/virtual path/uri to raster
    bands:    ((band, description), (band, description),...)
    """
    ds = gdal.Open(filepath, gdal.GA_Update)
    for band, desc in enumerate(bands):
        rb = ds.GetRasterBand(band + 1)
        rb.SetDescription(desc)
    del ds


def add_args(subparser):
    parser = subparser.add_parser("set_band_description")
    parser.add_argument("--input_raster", help="path to geotiff")
    parser.add_argument("--label_map", help="path to file with class names")


def main(args):
    with open(args.label_map, "r") as f:
        bands = f.readlines()
    set_band_descriptions(args.input_raster, bands)
    print("Done!")
