import os.path
import tempfile
import maptools


def test_rotate(ideal_map_filename):

    for axes in [(0, 1), (0, 2), (1, 2)]:

        _, output_filename = tempfile.mkstemp()

        maptools.rotate(
            input_filename=ideal_map_filename,
            output_filename=output_filename,
            axes=axes,
        )

        assert os.path.exists(output_filename)
