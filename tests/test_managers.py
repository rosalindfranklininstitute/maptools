import os
import pathlib
import random
import secrets
import struct
import sys
import unittest

import numpy

from maptools import models, cli, managers  # , utils, engines

BASE_DIR = pathlib.Path(__file__).parent.parent
TEST_DATA_DIR = BASE_DIR / 'test_data'


class TestManagers(unittest.TestCase):
    def setUp(self) -> None:
        self.test_fn = TEST_DATA_DIR / f"file-{secrets.token_urlsafe(3)}.map"
        self.test_fn2 = TEST_DATA_DIR / f"file-{secrets.token_urlsafe(3)}.map"
        shape = random.choices(range(12, 52, 4), k=3)
        self.shape = shape
        with models.MapFile(self.test_fn, 'w') as mapfile:
            mapfile.data = numpy.random.rand(*shape)
            mapfile.voxel_size = 3.78

    def tearDown(self) -> None:
        try:
            os.remove(self.test_fn)
        except FileNotFoundError:
            pass
        try:
            os.remove(self.test_fn2)
        except FileNotFoundError:
            pass

    def test_view(self):
        """"""
        args = cli.cli(f"map view {self.test_fn}")
        ex = managers.view(args)
        self.assertEqual(0, ex)

    def test_edit(self):
        """"""
        args = cli.cli(f"map edit {self.test_fn} -o {self.test_fn2}")
        managers.edit(args)
        # no changes then both files should be exactly alike
        with models.MapFile(self.test_fn, file_mode='r') as map1, models.MapFile(self.test_fn2, file_mode='r') as map2:
            self.assertEqual(map1.nc, map2.nc)
            self.assertEqual(map1.nr, map2.nr)
            self.assertEqual(map1.ns, map2.ns)
            self.assertEqual(map1.nx, map2.nx)
            self.assertEqual(map1.ny, map2.ny)
            self.assertEqual(map1.nz, map2.nz)
            self.assertEqual(map1.x_length, map2.x_length)
            self.assertEqual(map1.y_length, map2.y_length)
            self.assertEqual(map1.z_length, map2.z_length)
            self.assertEqual(map1.alpha, map2.alpha)
            self.assertEqual(map1.beta, map2.beta)
            self.assertEqual(map1.gamma, map2.gamma)
            self.assertEqual(map1.mapc, map2.mapc)
            self.assertEqual(map1.mapr, map2.mapr)
            self.assertEqual(map1.maps, map2.maps)
            self.assertEqual(map1.amin, map2.amin)
            self.assertEqual(map1.amax, map2.amax)
            self.assertEqual(map1.amean, map2.amean)
            self.assertEqual(map1.ispg, map2.ispg)
            self.assertEqual(map1.nsymbt, map2.nsymbt)
            self.assertEqual(map1.lskflg, map2.lskflg)
            self.assertEqual(map1.s11, map2.s11)
            self.assertEqual(map1.s12, map2.s12)
            self.assertEqual(map1.s13, map2.s13)
            self.assertEqual(map1.s21, map2.s21)
            self.assertEqual(map1.s22, map2.s22)
            self.assertEqual(map1.s23, map2.s23)
            self.assertEqual(map1.s31, map2.s31)
            self.assertEqual(map1.s32, map2.s32)
            self.assertEqual(map1.s33, map2.s33)
            self.assertEqual(map1.t1, map2.t1)
            self.assertEqual(map1.t2, map2.t2)
            self.assertEqual(map1.t3, map2.t3)
            self.assertEqual(map1.extra, map2.extra)
            self.assertEqual(map1.map, map2.map)
            self.assertEqual(map1.machst, map2.machst)
            self.assertEqual(map1.rms, map2.rms)
            self.assertNotEqual(map1.nlabl, map2.nlabl)
            self.assertNotEqual(map1.name, map2.name)
            self.assertTrue(numpy.array_equal(map1.data, map2.data))
            self.assertEqual(map1.orientation, map2.orientation)
            self.assertEqual(map1.mode, map2.mode)
            self.assertEqual(map1.start, map2.start)
            self.assertEqual(map1.voxel_size, map2.voxel_size)
            self.assertNotEqual(map1.labels, map2.labels)

    def test_edit_change_orientation(self):
        """"""
        # orientation
        args = cli.cli(f"map edit {self.test_fn} --orientation=YZX")
        managers.edit(args)
        with models.MapFile(self.test_fn) as mapfile:
            self.assertEqual((2, 3, 1), mapfile.orientation.to_integers())

    def test_edit_change_mode(self):
        """Test that changing the mode:

        - preserves the data
        - preserves space information
        """
        # before the change
        with models.MapFile(self.test_fn) as mapfile:
            self.assertAlmostEqual(3.78, mapfile.voxel_size[0], places=6)
            self.assertAlmostEqual(3.78, mapfile.voxel_size[1], places=6)
            self.assertAlmostEqual(3.78, mapfile.voxel_size[2], places=6)
        # edit
        args = cli.cli(f"map edit {self.test_fn} --map-mode=1 -o {self.test_fn2}")
        managers.edit(args)
        # managers.view(cli.cli(f"map view --colour {self.test_fn}"))
        # args = cli.cli(f"map edit {self.test_fn} --map-mode=1 -o {self.test_fn2}")
        # managers.edit(args)
        # after the change
        with models.MapFile(self.test_fn2) as mapfile2:
            self.assertAlmostEqual(3.78, mapfile2.voxel_size[0], places=6)
            self.assertAlmostEqual(3.78, mapfile2.voxel_size[1], places=6)
            self.assertAlmostEqual(3.78, mapfile2.voxel_size[2], places=6)
        # managers.view(cli.cli(f"map view --colour {self.test_fn}"))

    def test_file_modes(self):
        """Demonstrate that modifying a file with r+b does not truncate file. Call file.truncate() to do so."""
        with open(self.test_fn, 'wb') as f:
            f.write(struct.pack('<10f', *(0.0,) * 10))
        with open(self.test_fn, 'rb') as g:
            data = struct.unpack('<10f', g.read(10 * 4))
            print(f"before: {data}")
        with open(self.test_fn, 'r+b') as h:
            print(f"{h.tell()}")
            h.write(struct.pack('<5f', *(1.0,) * 5))
        with open(self.test_fn, 'rb') as g:
            data = struct.unpack('<10f', g.read(10 * 4))
            print(f"after: {data}")

    def test_edit_with_label(self):
        """"""
        args = cli.cli(f"map edit {self.test_fn}")
        managers.edit(args)
        with models.MapFile(self.test_fn, colour=True) as mapfile:
            self.assertRegex(mapfile.get_label(0), r".*edit.*")

    def test_edit_with_outfile(self):
        """"""
        args = cli.cli(f"map edit {self.test_fn} -c -O zyx -o {self.test_fn2}")
        managers.edit(args)
        with models.MapFile(self.test_fn2, colour=True) as mapfile:
            self.assertRegex(mapfile.get_label(0), r".*copied.*")

    def test_create(self):
        """"""
        args = cli.cli(f"map create {self.test_fn} -O XYZ -V 1 1 1 -M 2")
        managers.create(args)
        with models.MapFile(self.test_fn, colour=True) as mapfile:
            print(mapfile)
            self.assertRegex(mapfile.get_label(0), r".*creat.*")

    def test_create_ad_hoc(self):
        """"""
        args = cli.cli(f"map create {self.test_fn} -O XYZ -V 1.9 9.1 7.1 -M 2 -S -5 -5 -5 -s 30 15 28")
        managers.create(args)
        with models.MapFile(self.test_fn, colour=True) as mapfile:
            print(mapfile)
            self.assertEqual((1, 2, 3), mapfile.orientation.to_integers())
            self.assertAlmostEqual(1.9, mapfile.voxel_size[0], places=6)
            self.assertAlmostEqual(9.1, mapfile.voxel_size[1], places=6)
            self.assertAlmostEqual(7.1, mapfile.voxel_size[2], places=6)
            self.assertEqual((-5, -5, -5), mapfile.start)
            self.assertEqual((28, 15, 30), mapfile.data.shape)
            print(mapfile.data)
            self.assertTrue(numpy.array_equal(numpy.zeros(shape=args.size[::-1], dtype=numpy.int8), mapfile.data))

    def test_create_random(self):
        """"""
        args = cli.cli(f"map create {self.test_fn} -O XYZ -M 12 -V 1 1 1 --voxel-values random")
        managers.create(args)
        with models.MapFile(self.test_fn) as mapfile:
            # how do we know it's random?
            # densities: min, max, mean and rms should all be different
            # the length of the set of these values should be 4
            self.assertEqual(4, len({mapfile.amin, mapfile.amax, mapfile.amean, mapfile.rms}))

    def test_resample(self):
        """"""
        args = cli.cli(f"map sample --factor=4 {self.test_fn}")
        managers.sample(args)
        c, r, s = self.shape
        with models.MapFile(self.test_fn) as mapfile:
            self.assertEqual((c // args.factor, r // args.factor, s // args.factor), mapfile.data.shape)
