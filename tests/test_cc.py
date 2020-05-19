import os.path
import tempfile
import selknam.maptools


def test_cc(ideal_map_filename, rec_map_filename):

    # Test cross correlation
    _, output_filename = tempfile.mkstemp()

    selknam.maptools.cc(
        input_filename1=ideal_map_filename,
        input_filename2=rec_map_filename,
        output_filename=output_filename,
    )

    assert os.path.exists(output_filename)

    # Test auto correlation
    _, output_filename = tempfile.mkstemp()

    selknam.maptools.cc(
        input_filename1=ideal_map_filename, output_filename=output_filename
    )

    assert os.path.exists(output_filename)
