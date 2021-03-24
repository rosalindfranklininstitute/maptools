#
# Copyright (C) 2020 RFI
#
# Author: James Parkhurst
#
# This code is distributed under the GPLv3 license, a copy of
# which is included in the root directory of this package.
#
import logging
from maptools.util import read, write


# Get the logger
logger = logging.getLogger(__name__)


def crop(
    input_filename, output_filename, roi=None,
):
    """
    Crop the map

    Args:
        input_filename (str): The input map filename
        output_filename (str): The output map filename
        roi (list): The region of interest

    """

    # Open the input file
    infile = read(input_filename)

    # Get the roi
    if roi is not None:
        z0, y0, x0, z1, y1, x1 = roi
    else:
        z0, y0, x0 = 0, 0, 0
        z1, y1, x1 = infile.data.shape
    assert z1 > z0
    assert y1 > y0
    assert x1 > x0

    # Get the subset of data
    logger.info("Cropping map with roi: %s" % list(roi))
    data = infile.data[z0:z1, y0:y1, x0:x1]

    # Write the output file
    write(output_filename, data, infile=infile)
