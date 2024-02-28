"""
This script trains an autoML model on 
"""

import argparse
import os
import pickle
from datetime import datetime, timedelta
import sys
from pathlib import Path

import tpot
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
)
from sklearn.model_selection import StratifiedKFold


def evaluate_rf(clf, X_test, y_test):
    y_pred = clf.predict(X_test)
    print(clf)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0, average="weighted")
    f1 = f1_score(y_test, y_pred, zero_division=0, average="weighted")
    print(f"Accuracy: {acc:.3f}\nPrecision: {prec:.3f}\nF1: {f1:.3f}")
    return acc, prec, f1


def print_results(y_true, y_pred):
    print(
        f"Accuracy: {accuracy_score(y_true, y_pred):.3f}\n"
        + f"Precision: {precision_score(y_true, y_pred, zero_division=0, average='weighted'):.3f}\n"
        + f"F1: {f1_score(y_true, y_pred, zero_division=0, average='weighted'):.3f}"
    )


def add_args(subparser):
    parser = subparser.add_parser("tpot_train")
    parser.add_argument(
        "--input", type=str, required=True, help="csv for model training"
    )

    parser.add_argument("--out_folder", type=str, required=True, help="output folder")

    parser.add_argument(
        "--out_prefix", type=str, required=True, help="output file prefix"
    )

    parser.add_argument("--generations", type=int, required=True, help="generations")

    parser.add_argument(
        "--population_size", type=int, required=True, help="population size"
    )

    parser.add_argument(
        "--scoring", type=str, required=False, default="accuracy", help="scoring"
    )

    parser.add_argument(
        "--sep", type=str, required=False, default=",", help="csv separator"
    )

    parser.add_argument(
        "--decimal", type=str, required=False, default=".", help="decimal separator"
    )

    parser.add_argument(
        "--remove_classes_smaller_than",
        type=int,
        required=False,
        default=None,
        help="Classes smaller than this value are removed. Default None",
    )


def main(args):
    if sys.platform == "win32":
        BOLD = RESET = ""
    else:
        BOLD = "\x1B[1m"
        RESET = "\x1b[0m"

    uid = datetime.now().strftime("%y%m%dT%H%M%S")
    basename, ext = os.path.splitext(os.path.basename(args.input))

    out_folder = Path(args.out_folder)
    out_folder.mkdir(parents=True, exist_ok=True)

    # Read csv
    df = pd.read_csv(args.input, sep=args.sep, decimal=args.decimal)

    dfY = df.iloc[:, 0]
    dfX = df.iloc[:, 1:]

    # Print info
    print(BOLD + "Columns. First one is chosen as target" + RESET)
    print("Index\t\tColumn")
    for i, col in enumerate(df.columns):
        print(f"{i}\t\t{col}")
    print()

    print(BOLD + "\nTarget class distribution" + RESET)
    print("label\tcount")
    dfY.value_counts()
    print()

    # Classes smaller than 6 are removed
    drop_classes = dfY.value_counts()[dfY.value_counts() < 6].index.values
    drop_series = ~dfY.isin(drop_classes)

    dfY = dfY.loc[drop_series]
    dfX = dfX.loc[drop_series, :]

    print("Classes smaller than 6 are removed:")
    print(drop_classes)
    print()

    # Final dataset
    X = dfX.to_numpy()
    y = dfY.to_numpy()

    print(f"Shape of X: {X.shape}")

    # Actual training

    seed = 42

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)

    train, test = next(skf.split(X, y))
    X_train = X[train, :]
    X_test = X[test, :]
    y_train = y[train]
    y_test = y[test]

    print("Processing...")

    tpotC = tpot.TPOTClassifier(
        generations=args.generations,
        population_size=args.population_size,
        verbosity=2,
        scoring=args.scoring,
        random_state=seed,
        cv=5,
        n_jobs=-1,
    )

    tpotC.fit(X_train, y_train)
    clf = tpotC.fitted_pipeline_
    print("Done")

    print("\n RUN STATISTICS:")
    print(tpotC.score(X_test, y_test))

    y_true = []
    y_pred_rf = []
    y_pred_automl = []

    for i, (train, test) in enumerate(skf.split(X, y)):
        X_train = X[train, :]
        X_test = X[test, :]
        y_train = y[train]
        y_test = y[test]

        print(BOLD + f"\nFold {i}:" + RESET)
        rf = RandomForestClassifier()

        rf.fit(X_train, y_train)
        clf.fit(X_train, y_train)

        print("\nRF:")
        acc, prec, f1 = evaluate_rf(rf, X_test, y_test)
        print("\nTPOT AutoML:")
        acc, prec, f1 = evaluate_rf(clf, X_test, y_test)

        y_pred_fold_rf = rf.predict(X_test)
        y_pred_fold_automl = clf.predict(X_test)

        y_true = np.concatenate((y_true, y_test))
        y_pred_rf = np.concatenate((y_pred_rf, y_pred_fold_rf))
        y_pred_automl = np.concatenate((y_pred_automl, y_pred_fold_automl))

    print(BOLD + "\n\nFINAL RESULTS:" + RESET)
    print("\nRF results:")
    print_results(y_true, y_pred_rf)

    print("\nTPOT AutoML results:")
    print_results(y_true, y_pred_automl)

    acc = accuracy_score(y_true, y_pred_automl)

    # Save the model
    output_name = out_folder / f"{args.out_prefix}_acc{acc:.4f}_{uid}.py"
    print(f"\nSaving model to {output_name}")
    tpotC.export(output_name)


if __name__ == "__main__":
    main()
