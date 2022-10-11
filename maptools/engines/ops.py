"""
Engines that perform standard operations on map data

Engines are arranged alphabetically
"""
import logging

import numpy

logger = logging.getLogger(__name__)


def cross_correlation(
    data1: numpy.ndarray, data2: numpy.ndarray | None = None, **kwargs
) -> numpy.ndarray:
    """Compute the cross correlation using the data from two MAPs"""
    # Compute the Fourier transform of the data
    fdata1 = numpy.fft.fftn((data1 - numpy.mean(data1)) / numpy.std(data1))

    # Transform data2
    if data2 is not None:
        fdata2 = numpy.fft.fftn((data2 - numpy.mean(data2)) / numpy.std(data2))
    else:
        fdata2 = fdata1

    # Compute the CC
    _cross_correlation = (
        numpy.fft.fftshift(numpy.real(numpy.fft.ifftn(fdata1 * numpy.conj(fdata2))))
        / fdata1.size
    )

    # Print some output
    logger.info(
        "Min CC = %f, Max CC = %f"
        % (_cross_correlation.min(), _cross_correlation.max())
    )

    # Return the CC
    return _cross_correlation


def grid_resample(array: numpy.ndarray, factor: int) -> numpy.ndarray:
    """resample the grid provided by array according to the factor specified"""
    resampled_array = array[::factor, ::factor, ::factor]
    return resampled_array
