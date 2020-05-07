#
# Copyright (C) 2020 RFI
#
# Author: James Parkhurst
#
# This code is distributed under the GPLv3 license, a copy of
# which is included in the root directory of this package.
#
import mrcfile
import os


def process_map(input_filename, output_filename, roi=None, threshold=None, scale=None):
    """
    Edit an mrc file

    """

    # Open the input file
    print("Reading %s" % input_filename)
    infile = mrcfile.mmap(input_filename)

    # Get the roi
    if roi is not None:
        x0, y0, z0, x1, y1, z1 = roi
    else:
        x0, y0, z0 = 0, 0, 0
        x1, y1, z1 = infile.data.shape[::-1]

    # Get the subset of data
    data = infile.data[z0:z1, y0:y1, x0:x1]

    # Scale the data
    if scale is not None:
        print("Scaling by %f" % scale)
        data = data * scale

    # Mask the data
    if threshold is not None:
        print("Min = %.2g / Max = %.2g / Threshold = %.2g" % (data.min(), data.max(), threshold))
        data = data * (data > threshold)

    # Write the output file
    print("Writing %s" % output_filename)
    print("ROI:")
    print("  x = %d -> %d" % (x0, x1))
    print("  y = %d -> %d" % (y0, y1))
    print("  z = %d -> %d" % (z0, z1))
    outfile = mrcfile.new(output_filename, overwrite=True)
    outfile.set_data(data)
    outfile.voxel_size = infile.voxel_size
    outfile.update_header_stats()
