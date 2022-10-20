import os
import pathlib
import random
import secrets
import unittest

from maptools import models, utils

BASE_DIR = pathlib.Path(__file__).parent.parent
TEST_DATA_DIR = BASE_DIR / "test_data"


class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:

        # random name
        cls.random_name = TEST_DATA_DIR / f"file-{secrets.token_urlsafe(3)}.map"
        # random size
        cls.cols, cls.rows, cls.sections = random.sample(range(10, 30), k=3)
        with models.MapFile(cls.random_name, "w") as mapfile:
            mapfile.data = utils.get_vol(cls.cols, cls.rows, cls.sections)
            # mapfile.data = voxel_size = 1.5

    @classmethod
    def tearDownClass(cls) -> None:
        """cleanup"""
        try:
            os.remove(cls.random_name)
        except FileNotFoundError:
            print(f"file {cls.random_name} already deleted!")

    def test_get_orientation(self):
        """"""
        # by default, orientation is XYZ
        with models.MapFile(self.random_name) as mapfile:
            self.assertIsInstance(mapfile.orientation, models.Orientation)
            self.assertEqual("X", mapfile.orientation.cols)
            self.assertEqual("Y", mapfile.orientation.rows)
            self.assertEqual("Z", mapfile.orientation.sections)
