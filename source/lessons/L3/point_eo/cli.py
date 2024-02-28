# __main__.py
import warnings

warnings.filterwarnings(
    "ignore",
    message="Warning: optional dependency `torch` is not available. - skipping import of NN models.",
)

import argparse
from .scripts import (
    sample_raster,
    analysis,
    tpot_train,
    predict,
    set_band_description,
    postprocess_prediction,
)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Available commands", dest="script")

    sample_raster.add_args(subparsers)
    analysis.add_args(subparsers)
    tpot_train.add_args(subparsers)
    predict.add_args(subparsers)
    set_band_description.add_args(subparsers)
    postprocess_prediction.add_args(subparsers)

    args = parser.parse_args()

    if args.script == "sample_raster":
        sample_raster.main(args)
    elif args.script == "analysis":
        analysis.main(args)
    elif args.script == "tpot_train":
        tpot_train.main(args)
    elif args.script == "predict":
        predict.main(args)
    elif args.script == "set_band_description":
        set_band_description.main(args)
    elif args.script == "postprocess_prediction":
        postprocess_prediction.main(args)


if __name__ == "__main__":
    main()
