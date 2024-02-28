import geopandas as gpd
import rasterio as rio
from pathlib import Path
from pprint import pprint


def add_args(subparser):
    parser = subparser.add_parser("sample_raster")
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--input_raster", type=str, required=True)
    parser.add_argument("--target", type=str, help="target column")
    parser.add_argument(
        "--rename_target", type=str, help="target column is renamed to this"
    )
    parser.add_argument(
        "--band_names", type=str, default=None, help="file with band names as rows"
    )
    parser.add_argument(
        "--dropna",
        type=int,
        default=None,
        help="drops rows with all values as this value",
    )
    parser.add_argument("--out_prefix", type=str, default="")
    parser.add_argument("--out_folder", type=str, default=".")
    parser.add_argument("--shp", action="store_true")


def main(args):
    # Read files
    gdf = gpd.read_file(args.input)
    src = rio.open(args.input_raster, windowed=True)
    print(f"Sampling raster {args.input_raster} using points from {args.input}")

    # Sample points
    coords = [(x, y) for x, y in zip(gdf.geometry.x, gdf.geometry.y)]
    gdf["rvalue"] = [x for x in src.sample(coords)]

    # Fix dataframe
    bands = [f"band{i}" for i in range(len(gdf["rvalue"][0]))]

    if args.band_names:
        with open(args.band_names) as f:
            lines = f.readlines()
        bandnames = [l.strip() for l in lines]
        print("Using bandnames:")
        pprint(bandnames)
        if len(bands) != len(bandnames):
            raise Exception(
                f"Mismatch in band names in file ({len(bandnames)})"
                f" and number of bands ({len(bands)})"
            )
        else:
            bands = bandnames

    # Handle situation where the target band has the same name as
    # one of the sample bands
    if args.target in bands:
        if not args.rename_target:
            raise Exception(
                "One of the band names is same as the target. Set --rename_target"
            )
        target = args.rename_target
        gdf = gdf.rename({args.target: target}, axis=1)
        print(
            f"Target column has same name as bands. Renamed target column to {target}"
        )
    elif args.rename_target:
        target = args.rename_target
        gdf = gdf.rename({args.target: target}, axis=1)
    else:
        target = args.target

    gdf[bands] = gdf["rvalue"].values.tolist()
    gdf[bands] = gdf[bands].astype(src.meta["dtype"])
    gdf = gdf.drop(["rvalue"], axis=1)

    # Create df for csv
    df = gdf[[target] + bands]

    if args.dropna:
        df = df.loc[~(df[bands] == 0).all(axis=1)]  # drop rows where all values zeros
    df = df.dropna().reset_index().drop(["index"], axis=1)

    # Saving
    shp_stem = Path(args.input).stem
    raster_stem = Path(args.input_raster).stem

    out_folder = Path(args.out_folder)
    out_folder.mkdir(parents=True, exist_ok=True)
    out_stem = Path(f"{raster_stem}__{shp_stem}__{args.target}")
    if args.out_prefix != "":
        out_stem = Path(f"{args.out_prefix}__{out_stem}")

    if args.shp:
        suffix = ".shp"
    else:
        suffix = ".geojson"

    gdf.to_file(out_folder / out_stem.with_suffix(suffix))
    df.to_csv(out_folder / out_stem.with_suffix(".csv"), index=False)
    print(f"Saved outputs to {str(out_folder / out_stem.with_suffix('.csv'))}")
