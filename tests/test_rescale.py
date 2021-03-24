import os.path
import tempfile
import maptools


def test_rescale(ideal_map_filename):

    for mean, sdev, vmin, vmax, scale, offset in [
        (0, 1, None, None, None, None),
        (None, None, 0, 1, None, None),
        (None, None, None, None, 10, 5),
    ]:

        _, output_filename = tempfile.mkstemp()

        maptools.rescale(
            input_filename=ideal_map_filename,
            output_filename=output_filename,
            mean=mean,
            sdev=sdev,
            vmin=vmin,
            vmax=vmax,
            scale=scale,
            offset=offset,
        )

        assert os.path.exists(output_filename)
