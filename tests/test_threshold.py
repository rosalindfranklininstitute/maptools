import os.path
import tempfile
import selknam.maptools


def test_threshold(ideal_map_filename):

    for normalize in [True, False]:

        for zero in [True, False]:

            _, output_filename = tempfile.mkstemp()

            selknam.maptools.threshold(
                input_filename=ideal_map_filename,
                output_filename=output_filename,
                threshold=0,
                normalize=normalize,
                zero=zero,
            )

            assert os.path.exists(output_filename)
