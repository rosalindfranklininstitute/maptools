import os
import pathlib
import random
import secrets
import sys
import unittest

import numpy

from maptools import models, utils

BASE_DIR = pathlib.Path(__file__).parent.parent
TEST_DATA_DIR = BASE_DIR / "test_data"


class TestMapFile(unittest.TestCase):
    def setUp(self) -> None:
        self.test_fn = TEST_DATA_DIR / f"test-{secrets.token_urlsafe(3)}.map"
        self.test_fn2 = TEST_DATA_DIR / f"test-{secrets.token_urlsafe(3)}.map"

    def tearDown(self) -> None:
        try:
            os.remove(self.test_fn)
        except FileNotFoundError:
            print(
                "test.map already deleted or not used in this test...", file=sys.stderr
            )
        try:
            os.remove(self.test_fn2)
        except FileNotFoundError:
            pass

    def test_create_empty(self):
        """"""
        with self.assertRaises(ValueError):
            with models.MapFile(self.test_fn, file_mode="w") as mapfile:
                # everything is None or the default value
                self.assertIsNone(mapfile.nc)
                self.assertIsNone(mapfile.nr)
                self.assertIsNone(mapfile.ns)
                self.assertEqual(2, mapfile.mode)
                self.assertEqual((0, 0, 0), mapfile.start)
                self.assertIsNone(mapfile.nx)
                self.assertIsNone(mapfile.ny)
                self.assertIsNone(mapfile.nz)
                self.assertIsNone(mapfile.x_length)
                self.assertIsNone(mapfile.y_length)
                self.assertIsNone(mapfile.z_length)
                self.assertEqual(90.0, mapfile.alpha)
                self.assertEqual(90.0, mapfile.beta)
                self.assertEqual(90.0, mapfile.gamma)
                self.assertEqual(1, mapfile.mapc)
                self.assertEqual(2, mapfile.mapr)
                self.assertEqual(3, mapfile.maps)
                self.assertIsNone(mapfile.amin)
                self.assertIsNone(mapfile.amax)
                self.assertIsNone(mapfile.amean)
                self.assertEqual(1, mapfile.ispg)
                self.assertEqual(0, mapfile.nsymbt)
                self.assertEqual(0, mapfile.lskflg)
                self.assertEqual(0.0, mapfile.s11)
                self.assertEqual(0.0, mapfile.s12)
                self.assertEqual(0.0, mapfile.s13)
                self.assertEqual(0.0, mapfile.s21)
                self.assertEqual(0.0, mapfile.s22)
                self.assertEqual(0.0, mapfile.s23)
                self.assertEqual(0.0, mapfile.s31)
                self.assertEqual(0.0, mapfile.s32)
                self.assertEqual(0.0, mapfile.s33)
                self.assertEqual((0,) * 15, mapfile.extra)
                self.assertEqual(b"MAP ", mapfile.map)
                self.assertEqual(bytes([68, 68, 0, 0]), mapfile.machst)
                self.assertEqual(0, mapfile.nlabl)
                self.assertIsNone(mapfile.cols)
                self.assertIsNone(mapfile.rows)
                self.assertIsNone(mapfile.sections)

    def test_create_with_data(self):
        """"""
        # create
        with models.MapFile(self.test_fn, file_mode="w") as mapfile:
            # set data
            mapfile.data = numpy.random.rand(10, 20, 30)  # sections, rows, cols
            # now the following should be automatically inferred from the data
            self.assertEqual(30, mapfile.nc)
            self.assertEqual(20, mapfile.nr)
            self.assertEqual(10, mapfile.ns)
            self.assertEqual(2, mapfile.mode)
            self.assertEqual((0, 0, 0), mapfile.start)
            self.assertEqual(30, mapfile.nx)
            self.assertEqual(20, mapfile.ny)
            self.assertEqual(10, mapfile.nz)
            self.assertEqual(30.0, mapfile.x_length)
            self.assertEqual(20.0, mapfile.y_length)
            self.assertEqual(10.0, mapfile.z_length)
            self.assertEqual(90.0, mapfile.alpha)
            self.assertEqual(90.0, mapfile.beta)
            self.assertEqual(90.0, mapfile.gamma)
            self.assertEqual(1, mapfile.mapc)
            self.assertEqual(2, mapfile.mapr)
            self.assertEqual(3, mapfile.maps)
            self.assertIsNotNone(mapfile.amin)
            self.assertIsNotNone(mapfile.amax)
            self.assertIsNotNone(mapfile.amean)
            self.assertEqual(1, mapfile.ispg)
            self.assertEqual(0, mapfile.nsymbt)
            self.assertEqual(0, mapfile.lskflg)
            self.assertEqual(0.0, mapfile.s11)
            self.assertEqual(0.0, mapfile.s12)
            self.assertEqual(0.0, mapfile.s13)
            self.assertEqual(0.0, mapfile.s21)
            self.assertEqual(0.0, mapfile.s22)
            self.assertEqual(0.0, mapfile.s23)
            self.assertEqual(0.0, mapfile.s31)
            self.assertEqual(0.0, mapfile.s32)
            self.assertEqual(0.0, mapfile.s33)
            self.assertEqual((0,) * 15, mapfile.extra)
            self.assertEqual(b"MAP ", mapfile.map)
            self.assertEqual(bytes([68, 68, 0, 0]), mapfile.machst)
            self.assertEqual(0, mapfile.nlabl)
            self.assertEqual(30, mapfile.cols)
            self.assertEqual(20, mapfile.rows)
            self.assertEqual(10, mapfile.sections)
            self.assertEqual(
                "Orientation(cols='X', rows='Y', sections='Z')",
                str(mapfile.orientation),
            )
            self.assertEqual((1.0, 1.0, 1.0), mapfile.voxel_size)
            self.assertEqual("float32", mapfile.data.dtype.name)
        # mapfile is closed
        # read
        with models.MapFile(self.test_fn) as mapfile2:
            self.assertEqual(30, mapfile2.nc)
            self.assertEqual(20, mapfile2.nr)
            self.assertEqual(10, mapfile2.ns)
            self.assertEqual(2, mapfile2.mode)
            self.assertEqual((0, 0, 0), mapfile2.start)
            self.assertEqual(30, mapfile2.nx)
            self.assertEqual(20, mapfile2.ny)
            self.assertEqual(10, mapfile2.nz)
            self.assertEqual(30.0, mapfile2.x_length)
            self.assertEqual(20.0, mapfile2.y_length)
            self.assertEqual(10.0, mapfile2.z_length)
            self.assertEqual(90.0, mapfile2.alpha)
            self.assertEqual(90.0, mapfile2.beta)
            self.assertEqual(90.0, mapfile2.gamma)
            self.assertEqual(1, mapfile2.mapc)
            self.assertEqual(2, mapfile2.mapr)
            self.assertEqual(3, mapfile2.maps)
            self.assertIsNotNone(mapfile2.amin)
            self.assertIsNotNone(mapfile2.amax)
            self.assertIsNotNone(mapfile2.amean)
            self.assertEqual(1, mapfile2.ispg)
            self.assertEqual(0, mapfile2.nsymbt)
            self.assertEqual(0, mapfile2.lskflg)
            self.assertEqual(0.0, mapfile2.s11)
            self.assertEqual(0.0, mapfile2.s12)
            self.assertEqual(0.0, mapfile2.s13)
            self.assertEqual(0.0, mapfile2.s21)
            self.assertEqual(0.0, mapfile2.s22)
            self.assertEqual(0.0, mapfile2.s23)
            self.assertEqual(0.0, mapfile2.s31)
            self.assertEqual(0.0, mapfile2.s32)
            self.assertEqual(0.0, mapfile2.s33)
            self.assertEqual((0,) * 15, mapfile2.extra)
            self.assertEqual(b"MAP ", mapfile2.map)
            self.assertEqual(bytes([68, 68, 0, 0]), mapfile2.machst)
            self.assertEqual(0, mapfile2.nlabl)
            self.assertEqual(30, mapfile2.cols)
            self.assertEqual(20, mapfile2.rows)
            self.assertEqual(10, mapfile2.sections)
            self.assertEqual(
                "Orientation(cols='X', rows='Y', sections='Z')",
                str(mapfile2.orientation),
            )
            self.assertEqual((1.0, 1.0, 1.0), mapfile2.voxel_size)
            self.assertEqual("float32", mapfile2.data.dtype.name)

    def test_create_standard_then_modify_to_nonstandard(self):
        """"""
        # create
        with models.MapFile(self.test_fn, file_mode="w") as mapfile:
            # set data
            mapfile.data = numpy.random.rand(10, 20, 30)  # sections, rows, cols
            print(f"{mapfile.data.shape}")
            print(f"{mapfile.orientation}")
            print(f"{mapfile.cols, mapfile.rows, mapfile.sections}")
            # change orientation to nonstandar YXZ
            mapfile.orientation = models.Orientation(cols="Y", rows="X", sections="Z")
            print(f"{mapfile.data.shape}")
            print(f"{mapfile.orientation}")
            print(f"{mapfile.cols, mapfile.rows, mapfile.sections}")
            # now the following should be automatically inferred from the data
            self.assertEqual(20, mapfile.nc)
            self.assertEqual(30, mapfile.nr)
            self.assertEqual(10, mapfile.ns)
            # change orientation to nonstandard YZX
            # S=10, R=20, C=30
            # C=30, R=20, S=10
            # X Y Z
            # Y Z X
            # C'=20, R'=10, S'=30
            mapfile.orientation = models.Orientation(cols="Y", rows="Z", sections="X")
            self.assertEqual(20, mapfile.nc)
            self.assertEqual(10, mapfile.nr)
            self.assertEqual(30, mapfile.ns)
            # change orientation to nonstandard YZX
            mapfile.orientation = models.Orientation(cols="Z", rows="Y", sections="X")
            # Z Y X
            self.assertEqual(10, mapfile.nc)
            self.assertEqual(20, mapfile.nr)
            self.assertEqual(30, mapfile.ns)
            # let's do all the other orientation permutations
            # Z X Y
            mapfile.orientation = models.Orientation(cols="Z", rows="X", sections="Y")
            self.assertEqual(10, mapfile.nc)
            self.assertEqual(30, mapfile.nr)
            self.assertEqual(20, mapfile.ns)
            # X Z Y
            mapfile.orientation = models.Orientation(cols="X", rows="Z", sections="Y")
            self.assertEqual(30, mapfile.nc)
            self.assertEqual(10, mapfile.nr)
            self.assertEqual(20, mapfile.ns)

        # mapfile is closed
        # read
        with models.MapFile(self.test_fn) as mapfile2:
            self.assertEqual(30, mapfile2.nc)
            self.assertEqual(10, mapfile2.nr)
            self.assertEqual(20, mapfile2.ns)
            self.assertEqual(2, mapfile2.mode)
            self.assertEqual((0, 0, 0), mapfile2.start)
            self.assertEqual(30, mapfile2.nx)
            self.assertEqual(10, mapfile2.ny)
            self.assertEqual(20, mapfile2.nz)
            self.assertEqual(30.0, mapfile2.x_length)
            self.assertEqual(10.0, mapfile2.y_length)
            self.assertEqual(20.0, mapfile2.z_length)
            self.assertEqual(90.0, mapfile2.alpha)
            self.assertEqual(90.0, mapfile2.beta)
            self.assertEqual(90.0, mapfile2.gamma)
            self.assertEqual(1, mapfile2.mapc)
            self.assertEqual(3, mapfile2.mapr)
            self.assertEqual(2, mapfile2.maps)
            self.assertIsNotNone(mapfile2.amin)
            self.assertIsNotNone(mapfile2.amax)
            self.assertIsNotNone(mapfile2.amean)
            self.assertEqual(1, mapfile2.ispg)
            self.assertEqual(0, mapfile2.nsymbt)
            self.assertEqual(0, mapfile2.lskflg)
            self.assertEqual(0.0, mapfile2.s11)
            self.assertEqual(0.0, mapfile2.s12)
            self.assertEqual(0.0, mapfile2.s13)
            self.assertEqual(0.0, mapfile2.s21)
            self.assertEqual(0.0, mapfile2.s22)
            self.assertEqual(0.0, mapfile2.s23)
            self.assertEqual(0.0, mapfile2.s31)
            self.assertEqual(0.0, mapfile2.s32)
            self.assertEqual(0.0, mapfile2.s33)
            self.assertEqual((0,) * 15, mapfile2.extra)
            self.assertEqual(b"MAP ", mapfile2.map)
            self.assertEqual(bytes([68, 68, 0, 0]), mapfile2.machst)
            self.assertEqual(0, mapfile2.nlabl)
            self.assertEqual(30, mapfile2.cols)
            self.assertEqual(10, mapfile2.rows)
            self.assertEqual(20, mapfile2.sections)
            self.assertEqual(
                "Orientation(cols='X', rows='Z', sections='Y')",
                str(mapfile2.orientation),
            )
            self.assertEqual((1.0, 1.0, 1.0), mapfile2.voxel_size)
            self.assertEqual("float32", mapfile2.data.dtype.name)

    def test_read_and_modify(self):
        """"""
        with models.MapFile(self.test_fn, file_mode="w") as mapfile:
            # set data
            mapfile.data = numpy.random.rand(10, 20, 30)  # sections, rows, cols
            self.assertEqual(30, mapfile.nc)
            self.assertEqual(20, mapfile.nr)
            self.assertEqual(10, mapfile.ns)
            self.assertEqual(2, mapfile.mode)
            self.assertEqual((0, 0, 0), mapfile.start)
            self.assertEqual(30, mapfile.nx)
            self.assertEqual(20, mapfile.ny)
            self.assertEqual(10, mapfile.nz)
            self.assertEqual(30.0, mapfile.x_length)
            self.assertEqual(20.0, mapfile.y_length)
            self.assertEqual(10.0, mapfile.z_length)
            self.assertEqual(90.0, mapfile.alpha)
            self.assertEqual(90.0, mapfile.beta)
            self.assertEqual(90.0, mapfile.gamma)
            self.assertEqual(1, mapfile.mapc)
            self.assertEqual(2, mapfile.mapr)
            self.assertEqual(3, mapfile.maps)
            self.assertIsNotNone(mapfile.amin)
            self.assertIsNotNone(mapfile.amax)
            self.assertIsNotNone(mapfile.amean)
            self.assertEqual(1, mapfile.ispg)
            self.assertEqual(0, mapfile.nsymbt)
            self.assertEqual(0, mapfile.lskflg)
            self.assertEqual(0.0, mapfile.s11)
            self.assertEqual(0.0, mapfile.s12)
            self.assertEqual(0.0, mapfile.s13)
            self.assertEqual(0.0, mapfile.s21)
            self.assertEqual(0.0, mapfile.s22)
            self.assertEqual(0.0, mapfile.s23)
            self.assertEqual(0.0, mapfile.s31)
            self.assertEqual(0.0, mapfile.s32)
            self.assertEqual(0.0, mapfile.s33)
            self.assertEqual((0,) * 15, mapfile.extra)
            self.assertEqual(b"MAP ", mapfile.map)
            self.assertEqual(bytes([68, 68, 0, 0]), mapfile.machst)
            self.assertEqual(0, mapfile.nlabl)
            self.assertEqual(30, mapfile.cols)
            self.assertEqual(20, mapfile.rows)
            self.assertEqual(10, mapfile.sections)
            self.assertEqual(
                "Orientation(cols='X', rows='Y', sections='Z')",
                str(mapfile.orientation),
            )
            self.assertEqual((1.0, 1.0, 1.0), mapfile.voxel_size)

        # read and modify
        with models.MapFile(self.test_fn, file_mode="r+") as mapfile2:
            self.assertEqual(30, mapfile2.nc)
            self.assertEqual(20, mapfile2.nr)
            self.assertEqual(10, mapfile2.ns)
            self.assertEqual(1, mapfile2.mapc)
            self.assertEqual(2, mapfile2.mapr)
            self.assertEqual(3, mapfile2.maps)
            # change the orientation
            mapfile2.orientation = models.Orientation(cols="Z", rows="Y", sections="X")
            self.assertEqual(10, mapfile2.nc)
            self.assertEqual(20, mapfile2.nr)
            self.assertEqual(30, mapfile2.ns)
            self.assertEqual(3, mapfile2.mapc)
            self.assertEqual(2, mapfile2.mapr)
            self.assertEqual(1, mapfile2.maps)
            print(mapfile2)

    def test_voxel_size(self):
        """"""
        # we start off with a standard orientation but anisotropic
        # then we change to nonstandard
        # examine the voxel size
        with models.MapFile(self.test_fn, file_mode="w") as mapfile:
            mapfile.data = numpy.random.rand(3, 4, 5)
            # x=1.7, y=2.4, z=9.3
            # X=8.5, Y=9.6, Z=27.9
            mapfile.voxel_size = 1.7, 2.4, 9.3
            self.assertEqual(8.5, mapfile.x_length)
            self.assertEqual(9.6, mapfile.y_length)
            self.assertAlmostEqual(27.9, mapfile.z_length)
            # what if we change the orientation to ZYX
            mapfile.orientation = models.Orientation(cols="Z", rows="Y", sections="X")
            # the voxel sizes also get permuted
            self.assertEqual((9.3, 2.4, 1.7), mapfile.voxel_size)
            # but the lengths should change because we now have a different number of voxels on the same length
            self.assertAlmostEqual(27.9, mapfile.x_length)
            self.assertEqual(9.6, mapfile.y_length)
            self.assertAlmostEqual(8.5, mapfile.z_length)
            voxel_size_orig = mapfile.voxel_size

        # read
        with models.MapFile(self.test_fn, "r+") as mapfile2:
            self.assertAlmostEqual(voxel_size_orig[0], mapfile2.voxel_size[0], places=6)
            self.assertAlmostEqual(voxel_size_orig[1], mapfile2.voxel_size[1], places=6)
            self.assertAlmostEqual(voxel_size_orig[2], mapfile2.voxel_size[2], places=6)

    def test_create_anisotropic_voxels(self):
        # create with anisotropic voxel sizes
        with models.MapFile(self.test_fn, "w", voxel_size=(3.7, 2.6, 1.5)) as mapfile:
            mapfile.data = numpy.random.rand(12, 22, 17)
            self.assertEqual((3.7, 2.6, 1.5), mapfile.voxel_size)

    def test_create_with_nonstardard_and_anisotropic(self):
        """"""
        with models.MapFile(
            self.test_fn,
            "w",
            orientation=models.Orientation(cols="Y", rows="Z", sections="X"),
            voxel_size=(3.7, 2.6, 1.5),
        ) as mapfile:
            mapfile.data = numpy.random.rand(12, 22, 17)
            self.assertEqual((2, 3, 1), mapfile.orientation.to_integers())
            self.assertEqual((2.6, 1.5, 3.7), mapfile.voxel_size)

    def test_create_with_map_mode(self):
        """"""
        with models.MapFile(
            self.test_fn,
            file_mode="w",
            map_mode=0,
            voxel_size=(8.7, 9.2, 1.2),
            orientation=models.Orientation.from_integers((2, 3, 1)),
        ) as mapfile:
            mapfile.data = numpy.random.randint(0, 1, size=(11, 9, 16))
            self.assertEqual(0, mapfile.mode)

    def test_change_map_mode_int(self):
        """"""
        # int to int valid: 0, 1, 3, 6
        # float to float valid: 2, 12
        # complex to complex: 3, 4
        # int to/from float invalid
        with models.MapFile(self.test_fn, "w", map_mode=0) as mapfile:
            mapfile.data = numpy.random.randint(0, 1, (5, 5, 5))
            self.assertEqual(1, mapfile.data.itemsize)
            mapfile.mode = 1
            self.assertEqual(2, mapfile.data.itemsize)
            mapfile.mode = 3
            self.assertEqual(4, mapfile.data.itemsize)
            # change back
            mapfile.mode = 0
            self.assertEqual(1, mapfile.data.itemsize)
            mapfile.mode = 1
            self.assertEqual(2, mapfile.data.itemsize)

        with self.assertWarns(UserWarning):
            with models.MapFile(self.test_fn, "r+") as mapfile2:
                mapfile2.mode = 2
                self.assertEqual(4, mapfile2.data.itemsize)

        with self.assertWarns(UserWarning):
            with models.MapFile(self.test_fn, "r+") as mapf3:
                mapf3.mode = 1
                self.assertEqual(2, mapf3.data.itemsize)

    def test_change_map_mode_float(self):
        """"""
        with models.MapFile(self.test_fn, "w") as mapfile:
            mapfile.data = numpy.random.rand(8, 8, 8)
            self.assertEqual(4, mapfile.data.itemsize)
            mapfile.mode = 12
            self.assertEqual(2, mapfile.data.itemsize)

        with self.assertWarns(UserWarning):
            with models.MapFile(self.test_fn, "r+") as mapfile2:
                mapfile2.mode = 0
                self.assertEqual(1, mapfile2.data.itemsize)

    def test_change_map_mode_valid_data(self):
        """"""
        # start with map_mode = 2
        with models.MapFile(
            self.test_fn,
            "w",
            start=(-5, -5, -5),
            voxel_size=(1.9, 2.6, 4.2),
            colour=True,
            orientation=models.Orientation.from_string("YZX"),
        ) as mapfile:
            mapfile.data = numpy.random.rand(10, 10, 10)
            print(mapfile)
            # change to map_mode = 0
            mapfile.mode = 0
            print(mapfile)
        # change to map_mode = 1
        with models.MapFile(self.test_fn, "r+", colour=True) as mapfile2:
            mapfile2.mode = 1
            print(mapfile2)
        # change to map_mode = 2 again, but obviously we've lost the data
        with models.MapFile(self.test_fn, "r+", colour=True) as mapfile3:
            mapfile3.mode = 2
            print(mapfile3)

    def test_start(self):
        """"""
        with models.MapFile(self.test_fn, "w", start=(3, 9, -11)) as mapfile:
            mapfile.data = numpy.random.rand(3, 5, 2)
            print(mapfile)
            self.assertEqual((3, 9, -11), mapfile.start)
            # change start
            mapfile.start = (58, 3, 4)
            print(mapfile)
            self.assertEqual((58, 3, 4), mapfile.start)
        # read
        with models.MapFile(self.test_fn) as mapfile2:
            self.assertEqual((58, 3, 4), mapfile2.start)

    def test_handle_labels(self):
        """"""
        with models.MapFile(TEST_DATA_DIR / "emd_5625.map", colour=True) as mapfile:
            self.assertTrue(len(mapfile.labels) == 1)
            self.assertEqual("::::EMDATABANK.org::::EMD-5625::::", mapfile.get_label(0))
            # add a new label
            mapfile.add_label("there is a new dog in town")
            self.assertEqual(2, len(mapfile.labels))
            self.assertEqual(2, mapfile.nlabl)
            # insert a label
            mapfile.insert_label("are you coming for lunch?")
            self.assertEqual(3, len(mapfile.labels))
            mapfile.add_label("extra 1")
            mapfile.add_label("extra 2")
            mapfile.add_label("extra 3")
            mapfile.add_label("extra 4")
            mapfile.add_label("extra 5")
            mapfile.add_label("extra 6")
            mapfile.add_label("extra 7")
            print(mapfile)
            with self.assertWarns(UserWarning):
                mapfile.add_label("extra 8")
            self.assertEqual(10, len(mapfile.labels))
            mapfile.del_label()
            self.assertEqual(9, len(mapfile.labels))
            mapfile.insert_label("this is where it ends", 4)
            self.assertEqual(10, len(mapfile.labels))
            with self.assertWarns(UserWarning):
                mapfile.insert_label("another way to end", 7)

            # invalid values
            with self.assertWarns(UserWarning):
                mapfile.get_label(-11)
            with self.assertWarns(UserWarning):
                mapfile.get_label(10)
            with self.assertWarns(UserWarning):
                mapfile.add_label(
                    "I'm very sure that this is much longer than 80 characters because at some point I will cross "
                    "the 80 char limit line, right?"
                )
            with self.assertWarns(UserWarning):
                mapfile.insert_label("invalid label", 20)

            # clear all labels
            mapfile.clear_labels()
            self.assertEqual(0, len(mapfile.labels))
            print(mapfile)
            self.assertEqual(0, mapfile.nlabl)

            # unicode
            with self.assertWarns(UserWarning):
                mapfile.add_label("ニシコクマルガラスは私のクォーツのスフィンクスが大好きです")

            print(mapfile)

    def test_create_with_labels(self):
        """"""
        with models.MapFile(self.test_fn, "w", colour=True) as mapfile:
            mapfile.data = numpy.random.rand(5, 6, 7)
            mapfile.add_label("a new label")
            self.assertEqual("a new label", mapfile.get_label(0))
            mapfile.add_label("ニシコクマルガラスは私のクォーツのスフィンクスが大好きです")

        # read
        with models.MapFile(self.test_fn, colour=True) as mapfile2:
            self.assertEqual("a new label", mapfile2.get_label(0))
            self.assertEqual("ニシコクマルガラスは私のクォーツのスフィンクスが大好", mapfile2.get_label(1))
            print(mapfile2)

    def test_copy(self):
        """"""
        mapfile1 = models.MapFile(self.test_fn, "w")
        mapfile1.data = numpy.random.rand(2, 3, 4)
        # second one
        mapfile2 = models.MapFile(self.test_fn2, "w")
        mapfile2.copy(mapfile1)
        self.assertEqual(mapfile1, mapfile2)
        mapfile1.close()
        mapfile2.close()


class TestOrientation(unittest.TestCase):
    """
    `maptools` provides a simple API to
    """

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

    def test_orientation(self):
        """"""
        orientation = models.Orientation(cols="X", rows="Y", sections="Z")
        self.assertEqual("X", orientation.cols)
        self.assertEqual("Y", orientation.rows)
        self.assertEqual("Z", orientation.sections)
        self.assertEqual((1, 3), orientation.shape)
        self.assertEqual(
            "Orientation(cols='X', rows='Y', sections='Z')", repr(orientation)
        )
        self.assertEqual(
            "Orientation(cols='X', rows='Y', sections='Z')", str(orientation)
        )
        self.assertIsInstance(numpy.asarray(orientation), numpy.ndarray)
        self.assertEqual((1, 3), orientation.shape)
        # initialisation errors
        # must use x, y, z
        with self.assertRaises(ValueError):
            models.Orientation(cols="W", rows="Y", sections="Z")
        # can use lowercase
        orientation = models.Orientation(cols="x", rows="y", sections="z")
        self.assertEqual("X", orientation.cols)
        self.assertEqual("Y", orientation.rows)
        self.assertEqual("Z", orientation.sections)
        # no repetition of axes
        with self.assertRaises(ValueError):
            models.Orientation(cols="X", rows="X", sections="Y")
        # order doesn't matter
        orientation = models.Orientation(rows="Y", sections="X", cols="Z")
        self.assertEqual("Z", orientation.cols)
        self.assertEqual("Y", orientation.rows)
        self.assertEqual("X", orientation.sections)
        # create from integers using classmethod
        orientation = models.Orientation.from_integers((1, 2, 3))
        self.assertEqual("X", orientation.cols)
        self.assertEqual("Y", orientation.rows)
        self.assertEqual("Z", orientation.sections)
        # create from string using classmethod
        orientation = models.Orientation.from_string("YxZ")
        self.assertEqual("Y", orientation.cols)
        self.assertEqual("X", orientation.rows)
        self.assertEqual("Z", orientation.sections)

    def test_orientation_ops(self):
        """"""
        orientation1 = models.Orientation(cols="X", rows="Y", sections="Z")
        orientation2 = models.Orientation(cols="X", rows="Y", sections="Z")
        # trivial: the identity
        permutation_matrix = orientation1 / orientation2
        print(permutation_matrix)
        self.assertEqual(
            models.PermutationMatrix(numpy.eye(3, dtype=int)), permutation_matrix
        )
        # swap X and Z
        orientation1 = models.Orientation(cols="X", rows="Y", sections="Z")
        orientation2 = models.Orientation(cols="Z", rows="Y", sections="X")
        permutation_matrix = orientation1 / orientation2
        print(permutation_matrix)
        self.assertEqual(
            models.PermutationMatrix(
                numpy.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]], dtype=int)
            ),
            permutation_matrix,
        )
        # Z Y X -> Z X Y
        orientation1 = models.Orientation(cols="Z", rows="Y", sections="X")
        orientation2 = models.Orientation(cols="Z", rows="X", sections="Y")
        permutation_matrix = orientation1 / orientation2
        print(permutation_matrix)
        self.assertEqual(
            models.PermutationMatrix(
                numpy.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=int)
            ),
            permutation_matrix,
        )

    def test_from_integers(self):
        """"""
        orientation = models.Orientation.from_integers((2, 1, 3))
        self.assertIsInstance(orientation, models.Orientation)
        self.assertEqual("Y", orientation.cols)
        self.assertEqual("X", orientation.rows)
        self.assertEqual("Z", orientation.sections)

        with self.assertRaises(ValueError):
            models.Orientation.from_integers((1, 1, 3))

    def test_from_string(self):
        """"""
        orientation = models.Orientation.from_string("XZY")
        self.assertIsInstance(orientation, models.Orientation)
        self.assertEqual("X", orientation.cols)
        self.assertEqual("Z", orientation.rows)
        self.assertEqual("Y", orientation.sections)

        with self.assertRaises(ValueError):
            models.Orientation.from_string("XXY")

    def test_to_integers(self):
        """"""
        orientation = models.Orientation.from_string("XZY")
        self.assertEqual((1, 3, 2), orientation.to_integers())


class TestPermutationMatrix(unittest.TestCase):
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

    def test_permutation_matrix(self):
        """"""
        permutation_matrix = models.PermutationMatrix(numpy.eye(3, dtype=float))
        self.assertIsInstance(permutation_matrix, models.PermutationMatrix)
        self.assertEqual((3, 3), permutation_matrix.shape)
        self.assertEqual(3, permutation_matrix.rows)
        self.assertEqual(3, permutation_matrix.cols)
        self.assertEqual(int, permutation_matrix.dtype)
        # invalid data
        with self.assertRaises(ValueError):
            models.PermutationMatrix(
                numpy.fromstring("0 0 0 0 0 0 0 0 1", sep=" ").reshape(3, 3)
            )
        # non-binary
        with self.assertRaises(ValueError):
            models.PermutationMatrix(
                numpy.fromstring("1 0 0 0 2 0 0 0 1", sep=" ").reshape(3, 3)
            )

    def test_permuation_matrix_from_orientations(self):
        """"""
        permutation_matrix = models.PermutationMatrix.from_orientations(
            (1, 2, 3), (1, 3, 2)
        )
        self.assertIsInstance(permutation_matrix, models.PermutationMatrix)
        self.assertEqual((3, 3), permutation_matrix.shape)
        self.assertEqual(3, permutation_matrix.rows)
        self.assertEqual(3, permutation_matrix.cols)
        self.assertEqual(int, permutation_matrix.dtype)
        self.assertTrue(
            numpy.array_equal(
                numpy.fromstring("1 0 0 0 0 1 0 1 0", sep=" ", dtype=int).reshape(3, 3),
                numpy.asarray(permutation_matrix),
            )
        )

    def test_permutation_matrix_ops(self):
        """"""
        permutation_matrix1 = models.PermutationMatrix(
            numpy.fromstring("0 1 0 1 0 0 0 0 1", sep=" ", dtype=int).reshape(3, 3)
        )
        # LHS multiplication
        col_vector = numpy.fromstring("1 2 3", sep=" ", dtype=int).reshape(3, 1)
        product = permutation_matrix1 @ col_vector
        self.assertTrue(
            numpy.array_equal(
                numpy.fromstring("2 1 3", sep=" ", dtype=int).reshape(3, 1), product
            )
        )
        # RHS multiplication
        row_vector = numpy.fromstring("1 2 3", sep=" ", dtype=int).reshape(1, 3)
        product = row_vector @ permutation_matrix1
        self.assertTrue(
            numpy.array_equal(
                numpy.fromstring("2 1 3", sep=" ", dtype=int).reshape(1, 3), product
            )
        )
        # iRHS multiplication
        permutation_matrix1 @= permutation_matrix1
        self.assertTrue(
            numpy.array_equal(
                numpy.eye(3, dtype=int), numpy.asarray(permutation_matrix1)
            )
        )

    def test_swap_sequences(self):
        """Since the shape is ZYX, the swap axes should be 'inverted' i.e. if we are to swap X and Y instead of
        swapping 0 1 we swap 1 2"""
        swap_sequences = models.PermutationMatrix.from_orientations(
            (1, 2, 3), (1, 2, 3)
        ).swap_sequences
        self.assertEqual([], swap_sequences)
        swap_sequences = models.PermutationMatrix.from_orientations(
            (1, 2, 3), (1, 3, 2)
        ).swap_sequences
        self.assertEqual([(0, 1)], swap_sequences)
        swap_sequences = models.PermutationMatrix.from_orientations(
            (1, 2, 3), (2, 1, 3)
        ).swap_sequences
        self.assertEqual([(1, 2)], swap_sequences)
        swap_sequences = models.PermutationMatrix.from_orientations(
            (1, 2, 3), (2, 3, 1)
        ).swap_sequences
        self.assertEqual([(1, 2), (0, 2)], swap_sequences)
        swap_sequences = models.PermutationMatrix.from_orientations(
            (1, 2, 3), (3, 2, 1)
        ).swap_sequences
        self.assertEqual([(0, 2)], swap_sequences)
        swap_sequences = models.PermutationMatrix.from_orientations(
            (1, 2, 3), (3, 1, 2)
        ).swap_sequences
        self.assertEqual([(0, 2), (0, 1)], swap_sequences)
