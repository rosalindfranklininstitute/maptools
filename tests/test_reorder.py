import os.path
import tempfile
import maptools


def test_reorder(ideal_map_filename):

    _, output_filename = tempfile.mkstemp()

    maptools.reorder(
        input_filename=ideal_map_filename,
        output_filename=output_filename,
        axis_order=(0, 1, 2),
    )

    assert os.path.exists(output_filename)
