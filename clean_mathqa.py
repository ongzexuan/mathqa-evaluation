"""
Script of functions to clean up MathQA dataset. Currently (10/10/20), only cleans up the options fields.

Initially envisioned as a library for parsing the options data in the MathQA dataset.
Eventually decided it was easier to just normalize the data once and for all.

Goal: take the original MathQA dataset, and normalize the numeric options. This includes:
    - normalizing the format of options, explicitly separating them as a list
    - stripping special unicode characters
    - standardizing representations e.g. fractions and mixed numbers

Note: we manually preprocessed test.json such that there are only fractions "/" and ratios ":" left in the options
    text. They are treated as mathematically identical (can be resolved to a singular number).

I believe there may still be a sliver of value in retaining the original value representations. As such I append
the processed information as new fields in the output JSON.
"""

from utils import extract_options

import argparse
import json


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process / Clean up original MathQA dataset")
    parser.add_argument("--input", type=str, default="data/test.json")
    parser.add_argument("--output", type=str, default="out.json")
    args = parser.parse_args()

    # Parse input
    with open(args.input, "r") as f:
        data = json.load(f)

    # Process
    for datum in data:
        datum["processed_options"] = extract_options(datum["options"])
        print(datum["processed_options"])

    # Dump to output
    with open(args.output, "w") as f:
        json.dump(data, f)
