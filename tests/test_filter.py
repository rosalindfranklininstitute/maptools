import os.path
import tempfile
import maptools


def test_filter(ideal_map_filename):

    for filter_type in ["lowpass", "highpass", "bandpass", "bandstop"]:
        for filter_shape in ["square", "gaussian"]:

            if filter_shape == "gaussian" and filter_type != "lowpass":
                continue

            if filter_type in ("lowpass", "highpass"):
                resolution = 5
            else:
                resolution = 5, 8

            _, output_filename = tempfile.mkstemp()

            maptools.filter(
                input_filename=ideal_map_filename,
                output_filename=output_filename,
                filter_type=filter_type,
                filter_shape=filter_shape,
                resolution=resolution,
            )

            assert os.path.exists(output_filename)
