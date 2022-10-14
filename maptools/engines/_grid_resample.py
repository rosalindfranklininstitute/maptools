import numpy as np


def grid_resample(array: np.ndarray, factor: int):
    """resample the grid provided by array according to the factor specified"""
    resampled_array = array[::factor, ::factor, ::factor]
    return resampled_array
