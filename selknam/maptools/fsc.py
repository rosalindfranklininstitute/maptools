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
from matplotlib import pylab
from selknam.maptools.util import read, read_axis_order
from selknam.maptools.reorder import reorder


# Get the logger
logger = logging.getLogger(__name__)


def array_fsc(data1, data2, nbins=20, resolution=None, voxel_size=(1, 1, 1), **kwargs):
    """
    Compute the local FSC of the map

    Args:
        data1 (array): The input map 1
        data2 (array): The input map 2
        kernel (int): The kernel size
        nbins (int): The number of bins
        resolution (float): The resolution limit

    Returns:
        array: The FSC

    """

    # Get the subset of data
    logger.info("Computing FSC")

    # Normalize the data
    data1 = (data1 - numpy.mean(data1)) / numpy.std(data1)
    data2 = (data2 - numpy.mean(data2)) / numpy.std(data2)

    # Compute the radius
    shape = data1.shape
    Z, Y, X = numpy.mgrid[0 : shape[0], 0 : shape[1], 0 : shape[2]]
    Z = (1.0 / voxel_size["z"]) * (Z - shape[0] // 2) / shape[0]
    Y = (1.0 / voxel_size["y"]) * (Y - shape[1] // 2) / shape[1]
    X = (1.0 / voxel_size["x"]) * (X - shape[2] // 2) / shape[2]
    R = numpy.sqrt(X ** 2 + Y ** 2 + Z ** 2).flatten()

    # Compute the FFT of the data
    X = numpy.fft.fftshift(numpy.fft.fftn(data1)).flatten()
    Y = numpy.fft.fftshift(numpy.fft.fftn(data2)).flatten()

    # Create a resolution mask
    if resolution is not None:
        mask = R < 1.0 / resolution
        X = X[mask]
        Y = Y[mask]
        R = R[mask]
    else:
        resolution = 1 / R.max()

    # Scale R to number of bins
    R = numpy.floor(nbins * R / R.max()).astype("int32")

    # Compute local variance and covariance
    N = numpy.bincount(R)
    varX = numpy.bincount(R, numpy.abs(X) ** 2) / N
    varY = numpy.bincount(R, numpy.abs(Y) ** 2) / N
    covXY = numpy.bincount(R, numpy.real(X * numpy.conj(Y))) / N

    # Compute the FSC
    fsc = numpy.zeros(covXY.shape)
    tiny = 1e-5
    mask = (varX > tiny) & (varY > tiny)
    fsc[mask] = covXY[mask] / (numpy.sqrt(varX[mask]) * numpy.sqrt(varY[mask]))

    # Print some output
    logger.info("Resolution, FSC")
    bins = []
    for i in range(len(fsc)):
        step = (1.0 / resolution) / (nbins + 1)
        bins.append(((i + 1) * step))
        logger.info("%.2f, %.2f" % (1 / bins[i], fsc[i]))

    # Return the fsc
    return bins, fsc


def mapfile_fsc(
    input_filename1, input_filename2, output_filename=None, nbins=20, resolution=None
):
    """
    Compute the local FSC of the map

    Args:
        input_filename1 (str): The input map filename
        input_filename2 (str): The input map filename
        output_filename (str): The output map filename
        nbins (int): The number of bins
        resolution (float): The resolution limit

    """

    # Open the input files
    infile1 = read(input_filename1)
    infile2 = read(input_filename2)

    # Get the data
    data1 = infile1.data
    data2 = infile2.data

    # Reorder data2 to match data1
    data2 = reorder(data2, read_axis_order(infile2), read_axis_order(infile1))

    # Compute the FSC
    bins, fsc = array_fsc(
        data1, data2, voxel_size=infile1.voxel_size, nbins=nbins, resolution=resolution
    )

    # Write the FSC curve
    fig, ax = pylab.subplots(figsize=(8, 6))
    ax.plot(bins, fsc)
    ax.set_xlabel("Resolution 1/A")
    ax.set_ylabel("FSC")
    ax.set_ylim(0, 1)
    fig.savefig(output_filename, dpi=300, bbox_inches="tight")


def fsc(*args, **kwargs):
    """
    Compute the FSC of the map

    """
    if len(args) > 0 and type(args[0]) == "str" or "input_filename1" in kwargs:
        func = mapfile_fsc
    else:
        func = array_fsc
    return func(*args, **kwargs)
