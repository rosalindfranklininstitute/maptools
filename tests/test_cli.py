import pathlib
import pathlib
import unittest

from maptools import cli  # , managers, utils, engines

BASE_DIR = pathlib.Path(__file__).parent.parent
TEST_DATA_DIR = BASE_DIR / "test_data"


class TestCLI(unittest.TestCase):
    def test_view(self):
        """"""
        args = cli.cli(f"map view file.map")
        self.assertEqual("view", args.command)
        self.assertEqual("file.map", args.file)
        self.assertFalse(args.verbose)
        self.assertFalse(args.colour)

    def test_edit(self):
        args = cli.cli(f"map edit file.map")
        self.assertEqual("edit", args.command)
        self.assertEqual("file.map", args.file)
        self.assertIsNone(args.orientation)
        self.assertIsNone(args.voxel_sizes)
        self.assertEqual("r+", args.file_mode)
        self.assertEqual([0, 0, 0], args.start)
        self.assertIsNone(args.map_mode)
        self.assertFalse(args.verbose)
        self.assertFalse(args.colour)

    def test_create_with_no_arguments(self):
        args = cli.cli(f"map create file.map")
        # self.assertEqual('create', args.command)
        self.assertIsNone(args.command)
        self.assertEqual("file.map", args.file)
        self.assertIsNone(args.orientation)
        self.assertIsNone(args.voxel_sizes)
        self.assertEqual([10, 10, 10], args.size)
        self.assertEqual("w", args.file_mode)
        self.assertEqual([0, 0, 0], args.start)
        self.assertIsNone(args.map_mode)
        self.assertEqual(0, args.min)
        self.assertEqual(10, args.max)
        self.assertEqual("zeros", args.voxel_values)
        self.assertFalse(args.verbose)
        self.assertFalse(args.colour)

    def test_create_with_arguments(self):
        args = cli.cli(f"map create file.map -O yzx -M 0 -V 3.0 2.0 1.0")
        self.assertEqual("create", args.command)
        self.assertEqual("file.map", args.file)
        self.assertEqual("YZX", args.orientation)
        self.assertAlmostEqual(3.0, args.voxel_sizes[0])
        self.assertAlmostEqual(2.0, args.voxel_sizes[1])
        self.assertAlmostEqual(1.0, args.voxel_sizes[2])
        self.assertEqual([10, 10, 10], args.size)
        self.assertEqual("w", args.file_mode)
        self.assertEqual([0, 0, 0], args.start)
        self.assertEqual(0, args.map_mode)
        self.assertEqual(0, args.min)
        self.assertEqual(10, args.max)
        self.assertEqual("zeros", args.voxel_values)
        self.assertFalse(args.verbose)
        self.assertFalse(args.colour)

    def test_sample(self):
        """"""
        args = cli.cli(f"map sample --factor 2 file.map")
        self.assertEqual("sample", args.command)
        self.assertEqual(2, args.factor)
        self.assertEqual("file.map", args.file)

    def test_ops(self):
        """The ops command"""
        args = cli.cli(f"map ops")
        print(args)
        self.assertEqual("ops", args.command)
