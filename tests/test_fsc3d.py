import os.path
import tempfile
import selknam.maptools


def test_fsc3d(ideal_map_filename, rec_map_filename):

    for axes in [0, 1, 2, (0, 1), (0, 2), (1, 2), (0, 1, 2), None]:

        _, output_filename = tempfile.mkstemp()

        selknam.maptools.fsc3d(
            input_filename1=ideal_map_filename,
            input_filename2=rec_map_filename,
            output_filename=output_filename,
            kernel=9,
            resolution=3,
        )

        assert os.path.exists(output_filename)
