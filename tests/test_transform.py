import os.path
import tempfile
import selknam.maptools


def test_transform(ideal_map_filename):

    _, output_filename = tempfile.mkstemp()

    selknam.maptools.transform(
        input_filename=ideal_map_filename,
        output_filename=output_filename,
        offset=None,
        rotation=(0, 45, 0),
        translation=(10, 10, 10),
        deg=True,
    )

    assert os.path.exists(output_filename)
