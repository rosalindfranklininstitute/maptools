import os.path
import tempfile
import maptools


def test_fsc(ideal_map_filename, rec_map_filename):

    for axis in [0, 1, 2, (0, 1), (0, 2), (1, 2), (0, 1, 2), None]:

        _, output_filename = tempfile.mkstemp()

        maptools.fsc(
            input_filename1=ideal_map_filename,
            input_filename2=rec_map_filename,
            output_filename=output_filename,
            nbins=20,
            resolution=3,
            axis=axis,
        )

        assert os.path.exists(output_filename)
