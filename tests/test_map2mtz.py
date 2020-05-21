import os.path
import tempfile
import selknam.maptools


def test_map2mtz(ideal_map_filename):

    _, output_filename = tempfile.mkstemp()

    selknam.maptools.map2mtz(
        input_filename=ideal_map_filename,
        output_filename=output_filename,
        resolution=8,
    )

    assert os.path.exists(output_filename)
