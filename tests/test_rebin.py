import os.path
import tempfile
import selknam.maptools


def test_rebin(ideal_map_filename):

    _, output_filename = tempfile.mkstemp()

    selknam.maptools.rebin(
        input_filename=ideal_map_filename,
        output_filename=output_filename,
        shape=(25, 25, 25),
    )

    assert os.path.exists(output_filename)
