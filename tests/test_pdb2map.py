import os.path
import tempfile
import maptools


def test_pdb2map(pdb_filename):

    _, output_filename = tempfile.mkstemp()

    maptools.pdb2map(
        input_pdb_filename=pdb_filename,
        output_map_filename=output_filename,
        resolution=8,
        grid=(200, 200, 200),
    )

    assert os.path.exists(output_filename)
