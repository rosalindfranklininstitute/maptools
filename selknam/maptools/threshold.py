#
# Copyright (C) 2020 RFI
#
# Author: James Parkhurst
#
# This code is distributed under the GPLv3 license, a copy of
# which is included in the root directory of this package.
#
import logging
import numpy
from selknam.maptools.util import read, write


# Get the logger
logger = logging.getLogger(__name__)


def array_threshold(data, threshold=0, normalize=False, zero=True):
    """
    Threshold the map

    Args:
        data (array): The input data
        threshold (float): The threshold value
        normalize (bool): Normalize the map before thresholding
        zero (bool): Shift the data to zero

    Returns:
        array: The thresholded array

    """

    # Apply the threshold
    logger.info("Apply threshold %f" % threshold)
    if normalize:
        data = (data - numpy.mean(data)) / numpy.std(data)
    data[data < threshold] = threshold
    if zero:
        data -= threshold

    # Return the data
    return data


def mapfile_threshold(
    input_filename, output_filename, threshold=0, normalize=False, zero=True
):
    """
    Threshold the map

    Args:
        input_filename (str): The input map filename
        output_filename (str): The output map filename
        threshold (float): The threshold value
        normalize (bool): Normalize the map before thresholding
        zero (bool): Shift the data to zero

    """

    # Open the input file
    infile = read(input_filename)

    # Get data
    data = infile.data.copy()

    # Apply the threshold
    data = array_threshold(data, threshold=threshold, normalize=normalize, zero=zero)

    # Write the output file
    write(output_filename, data, infile=infile)


def threshold(*args, **kwargs):
    """
    Threshold the map

    """
    if len(args) > 0 and type(args[0]) == "str" or "input_filename" in kwargs:
        func = mapfile_threshold
    else:
        func = array_threshold
    return func(*args, **kwargs)
