#
# Copyright (C) 2020 RFI
#
# Author: James Parkhurst
#
# This code is distributed under the GPLv3 license, a copy of
# which is included in the root directory of this package.
#
import numpy
import mrcfile
from math import sqrt, log


def process_map(
    input_filename,
    output_filename,
    mask_filename=None,
    roi=None,
    threshold=None,
    threshold_type="abs",
    scale=None,
    resolution=None,
):
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

    # Apply a mask
    if mask_filename is not None:
        maskfile = mrcfile.open(mask_filename)
        maskdata = maskfile.data
    else:
        maskdata = None

    # Filter to a resolution. Use a guassian filter in fourier space with
    # HWHM = 1 / resolution
    if resolution is not None:
        voxel_size = (
            infile.voxel_size["z"],
            infile.voxel_size["y"],
            infile.voxel_size["x"],
        )
        fdata = numpy.fft.fftn(data)
        z, y, x = numpy.mgrid[
            0 : fdata.shape[0], 0 : fdata.shape[1], 0 : fdata.shape[2]
        ]
        z = (1 / voxel_size[0]) * (z - fdata.shape[0] // 2) / fdata.shape[0]
        y = (1 / voxel_size[1]) * (y - fdata.shape[1] // 2) / fdata.shape[1]
        x = (1 / voxel_size[2]) * (x - fdata.shape[2] // 2) / fdata.shape[2]
        r = numpy.sqrt(x ** 2 + y ** 2 + z ** 2)
        sigma = 1.0 / (sqrt(2 * log(2)) * resolution)
        mask = numpy.exp(-0.5 * (r / sigma) ** 2)
        mask = numpy.fft.fftshift(mask)
        fdata = fdata * mask
        data = numpy.real(numpy.fft.ifftn(fdata)).astype("float32")

    # Scale the data
    if scale is not None:
        print("Scaling by %f" % scale)
        data = data * scale

    # Mask the data
    if threshold is not None:
        if threshold_type is "abs":
            print(
                "Min = %.2g / Max = %.2g / Threshold = %.2g"
                % (data.min(), data.max(), threshold)
            )
            data = data * (data > threshold)
        else:
            if maskdata is None:
                mu = numpy.mean(data)
                sig = numpy.std(data)
            else:
                mu = numpy.mean(data[maskdata == 0])
                sig = numpy.std(data[maskdata == 0])
            mask = (data - mu) / sig > threshold
            data = data * mask * (data > 0)

    # Apply the maskdata
    if maskdata is not None:
        data = data * maskdata

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
