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
from matplotlib import pylab, ticker
from selknam.maptools.util import read, read_axis_order
from selknam.maptools.reorder import reorder
from math import sqrt


# Get the logger
logger = logging.getLogger(__name__)


def array_fsc(
    data1, data2, nbins=20, resolution=None, voxel_size=(1, 1, 1), axes=None, **kwargs
):
    """
    Compute the local FSC of the map

    Args:
        data1 (array): The input map 1
        data2 (array): The input map 2
        nbins (int): The number of bins
        resolution (float): The resolution limit
        axes (tuple): The axes of the plane to compute the FSC

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
    R = numpy.fft.fftshift(X ** 2 + Y ** 2 + Z ** 2)

    # Compute the FFT of the data
    X = numpy.fft.fftn(data1)
    Y = numpy.fft.fftn(data2)

    # Select the data along the selected axis
    if axes is not None:
        index = [0, 0, 0]
        for a in axes:
            index[a] = slice(None)
        index = tuple(index)
        X = X[index]
        Y = Y[index]
        R = R[index]

    # Flatten the array
    X = X.flatten()
    Y = Y.flatten()
    R = R.flatten()

    # Create a resolution mask
    if resolution is not None:
        mask = R < 1.0 / resolution ** 2
        X = X[mask]
        Y = Y[mask]
        R = R[mask]
    else:
        resolution = 1 / sqrt(R.max())

    # Multiply X and Y together
    XX = numpy.abs(X) ** 2
    YY = numpy.abs(Y) ** 2
    XY = numpy.real(X * numpy.conj(Y))

    # Compute local variance and covariance either by binning with resolution
    # or by computing a running mean
    # if nbins is not None and nbins > 0:
    bin_index = numpy.floor(nbins * R * resolution ** 2).astype("int32")
    varX = numpy.bincount(bin_index, XX)
    varY = numpy.bincount(bin_index, YY)
    covXY = numpy.bincount(bin_index, XY)
    bins = (1 / resolution ** 2) * numpy.arange(1, covXY.size + 1) / (covXY.size)

    # Compute the FSC
    tiny = 1e-5
    mask = (varX > tiny) & (varY > tiny)
    fsc = numpy.zeros(covXY.shape)
    fsc[mask] = covXY[mask] / (numpy.sqrt(varX[mask]) * numpy.sqrt(varY[mask]))

    # Print some output
    logger.info("Resolution, FSC")
    for b, f in zip(bins, fsc):
        logger.info("%.2f, %.2f" % (1 / sqrt(b), f))

    # Return the fsc
    return bins, fsc


def mapfile_fsc(
    input_filename1,
    input_filename2,
    output_filename=None,
    nbins=20,
    resolution=None,
    axes=None,
):
    """
    Compute the local FSC of the map

    Args:
        input_filename1 (str): The input map filename
        input_filename2 (str): The input map filename
        output_filename (str): The output map filename
        nbins (int): The number of bins
        resolution (float): The resolution limit
        axes (tuple): The axes of the plane to compute the FSC

    """

    # Open the input files
    infile1 = read(input_filename1)
    infile2 = read(input_filename2)

    # Get the data
    data1 = infile1.data
    data2 = infile2.data

    # Reorder data2 to match data1
    axis_order1 = read_axis_order(infile1)
    axis_order2 = read_axis_order(infile2)
    data2 = reorder(data2, axis_order2, axis_order1)

    # Reorder the axes to be in axis1 order
    if axes is not None:
        axes = tuple(axis_order1.index(a) for a in axes)

    # Compute the FSC
    bins, fsc = array_fsc(
        data1,
        data2,
        voxel_size=infile1.voxel_size,
        nbins=nbins,
        resolution=resolution,
        axes=axes,
    )

    # Write the FSC curve
    fig, ax = pylab.subplots(figsize=(8, 6))
    ax.plot(bins, fsc)
    ax.set_xlabel("Resolution (A)")
    ax.set_ylabel("FSC")
    ax.set_ylim(0, 1)
    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, p: "%.1f" % (1 / sqrt(x)) if x > 0 else None)
    )
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
