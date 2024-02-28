import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import rioxarray


def save_raster(x, name, crs):
    if not np.all(x == np.zeros_like(x)):
        x.rio.to_raster(name, compress="LZW", crs=crs, tiled=True, windowed=True)


def add_args(subparser):
    parser = subparser.add_parser("postprocess_prediction")

    parser.add_argument("--input_raster", type=str, required=True)
    parser.add_argument("--out_folder", type=str, required=True)
    parser.add_argument("--label_map", type=str)
    parser.add_argument("--crs", type=str, required=False, default="EPSG:3067")


def main(args):
    input_raster = Path(args.input_raster)
    out_folder = Path(args.out_folder)
    out_folder.mkdir(exist_ok=True, parents=True)

    chunk_s = 2**10
    xds = rioxarray.open_rasterio(
        args.input_raster,
        chunks={"band": -1, "x": chunk_s, "y": chunk_s},
        lock=False,
        parallel=True,
    )

    S = xds.argmax("band").astype("uint16")
    M = xds.max("band").astype("uint16")

    save_raster(S, out_folder / f"{input_raster.stem}_S.tif", args.crs)
    save_raster(M, out_folder / f"{input_raster.stem}_M.tif", args.crs)
    print("Saved S and M rasters")

    if args.label_map:
        with open(args.label_map) as f:
            fwd = {label.strip(): i for i, label in enumerate(f)}

        classes = list(fwd.keys())
        print(classes)

        cm = plt.get_cmap("tab20")

        def create_qgis_colormap(outname, classes):
            with open(outname, "w") as f:
                for i, classname in enumerate(classes):
                    rgb = list((np.array(cm(i)) * 255).astype(np.uint8))
                    f.write(str(i) + " ")
                    f.writelines([str(x) + " " for x in rgb])
                    f.write(str(classname) + "\n")

        create_qgis_colormap(
            Path(out_folder) / f"{input_raster.stem}_cmap.txt", classes
        )


if __name__ == "__main__":
    main()
    exit()
