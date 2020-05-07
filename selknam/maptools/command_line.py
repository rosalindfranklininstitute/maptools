#
# Copyright (C) 2020 RFI
#
# Author: James Parkhurst
#
# This code is distributed under the GPLv3 license, a copy of
# which is included in the root directory of this package.
#
import argparse
import os
import selknam.maptools


def main():
    """
    Edit an mrc file

    """
    # Create the command line parser
    parser = argparse.ArgumentParser(description="process a map")
    parser.add_argument("-o", dest="output", default=None, help="The output file")
    parser.add_argument(
        "-i", dest="input", default=None, required=True, help="The input file"
    )
    parser.add_argument("--roi", dest="roi", default=None, help="Set an ROI")
    parser.add_argument("--threshold", dest="threshold", type=float, default=None, help="Set a threshold")
    parser.add_argument("--scale", dest="scale", type=float, default=1, help="Scale the map")

    # Parse the arguments
    args = parser.parse_args()

    # Parse the ROI
    if args.roi is not None:
        x0, y0, z0, x1, y1, z1 = tuple(map(int, args.roi.split(",")))
        assert x1 > x0
        assert y1 > y0
        assert z1 > z0
        roi=(x0, y0, z0, x1, y1, z1)
    else:
        roi = None

    # Set the output filename
    if args.output is None:
        args.output = "%s_processed.mrc" % os.path.splitext(input_filename)[0]

    # Process the map
    selknam.maptools.process_map(
        input_filename=args.input,
        output_filename=args.output,
        roi=roi,
        threshold=args.threshold,
        scale=args.scale)
