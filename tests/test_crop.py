import os.path
import tempfile
import selknam.maptools


def test_crop(ideal_map_filename):

    _, output_filename = tempfile.mkstemp()

    selknam.maptools.crop(
        input_filename=ideal_map_filename,
        output_filename=output_filename,
        roi=(50, 60, 70, 100, 90, 80),
    )

    assert os.path.exists(output_filename)
