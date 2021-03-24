import os.path
import tempfile
import maptools


def test_fit(ideal_map_filename, pdb_filename):

    _, output_filename = tempfile.mkstemp()
    _, log_filename = tempfile.mkstemp()

    maptools.fit(
        input_map_filename=ideal_map_filename,
        input_pdb_filename=pdb_filename,
        output_pdb_filename=output_filename,
        mode="rigid_body",
        resolution=8,
        ncycle=2,
        log_filename=log_filename,
    )

    assert os.path.exists(output_filename)
