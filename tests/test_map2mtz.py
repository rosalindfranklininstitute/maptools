import os.path
import tempfile
import maptools


def test_map2mtz(ideal_map_filename):

    _, output_filename = tempfile.mkstemp()

    maptools.map2mtz(
        input_map_filename=ideal_map_filename,
        output_hkl_filename=output_filename,
        resolution=8,
    )

    assert os.path.exists(output_filename)
