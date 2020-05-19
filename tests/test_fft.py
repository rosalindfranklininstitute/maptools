import os.path
import tempfile
import selknam.maptools


def test_fft(ideal_map_filename):

    for mode in ["real", "imaginary", "amplitude", "phase", "power"]:
        for shift in [True, False]:
            for normalize in [True, False]:

                _, output_filename = tempfile.mkstemp()

                selknam.maptools.fft(
                    input_filename=ideal_map_filename,
                    output_filename=output_filename,
                    mode=mode,
                    shift=shift,
                    normalize=normalize,
                )

                assert os.path.exists(output_filename)
