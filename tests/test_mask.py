import os.path
import tempfile
import maptools


def test_mask(ideal_map_filename, mask_filename):

    for fourier_space in [True, False]:

        for shift in [True, False]:

            _, output_filename = tempfile.mkstemp()

            maptools.mask(
                input_filename=ideal_map_filename,
                output_filename=output_filename,
                mask_filename=mask_filename,
                fourier_space=fourier_space,
                shift=shift,
            )

            assert os.path.exists(output_filename)
