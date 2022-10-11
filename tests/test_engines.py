import pathlib
import unittest

from maptools import utils, engines

BASE_DIR = pathlib.Path(__file__).parent.parent
TEST_DATA_DIR = BASE_DIR / "test_data"


class TestEngines(unittest.TestCase):
    def test_grid_resample(self):
        vol = utils.get_vol(10, 10, 10)
        factor = 2
        resampled_vol = engines.grid_resample(vol, factor)
        self.assertEqual((5, 5, 5), resampled_vol.shape)
