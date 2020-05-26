#
# Copyright (C) 2020 RFI
#
# Author: James Parkhurst
#
# This code is distributed under the GPLv3 license, a copy of
# which is included in the root directory of this package.
#
import argparse
import logging
import selknam.maptools


def cc(args):
    """
    Compute map cc in real space

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.cc(
        input_filename1=args.input,
        input_filename2=args.input2,
        output_filename=args.output,
    )


def crop(args):
    """
    Crop a map

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.crop(
        input_filename=args.input, output_filename=args.output, roi=args.roi
    )


def edit(args):
    """
    Edit a map

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.edit(input_filename=args.input, voxel_size=args.voxel_size)


def fft(args):
    """
    Compute the map fft

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.fft(
        input_filename=args.input,
        output_filename=args.output,
        mode=args.mode,
        shift=args.shift,
        normalize=args.normalize,
    )


def filter(args):
    """
    Filter the map

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.filter(
        input_filename=args.input,
        output_filename=args.output,
        filter_type=args.type,
        filter_shape=args.shape,
        resolution=args.resolution,
    )


def fit(args):
    """
    Compute the map fit

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.fit(
        input_map_filename=args.input,
        input_pdb_filename=args.input2,
        output_pdb_filename=args.output,
        resolution=args.resolution,
        ncycle=args.ncycle,
        mode=args.mode,
        log_filename=args.logfile,
    )


def fsc(args):
    """
    Compute the map FSC

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.fsc(
        input_filename1=args.input,
        input_filename2=args.input2,
        output_filename=args.output,
        output_data_filename=args.output_data,
        nbins=args.nbins,
        resolution=args.resolution,
        axis=args.axis,
        method=args.method,
    )


def fsc3d(args):
    """
    Compute the local map FSC

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.fsc3d(
        input_filename1=args.input,
        input_filename2=args.input2,
        output_filename=args.output,
        kernel=args.kernel,
        resolution=args.resolution,
    )


def map2mtz(args):
    """
    Convert the map to an mtz file

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.map2mtz(
        input_filename=args.input,
        output_filename=args.output,
        resolution=args.resolution,
    )


def mask(args):
    """
    Mask the map

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.mask(
        input_filename=args.input,
        output_filename=args.output,
        mask_filename=args.mask,
        fourier_space=args.fourier_space,
        shift=args.shift,
    )


def pdb2map(args):
    """
    Convert the pdb file into a map file

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.pdb2map(
        input_filename=args.input,
        output_filename=args.output,
        resolution=args.resolution,
        grid=args.grid,
    )


def reorder(args):
    """
    Reorder the map axes

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.reorder(
        input_filename=args.input,
        output_filename=args.output,
        axis_order=args.axis_order,
    )


def rebin(args):
    """
    Resample the map

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.rebin(
        input_filename=args.input, output_filename=args.output, shape=args.shape
    )


def rescale(args):
    """
    Rescale the map

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.rescale(
        input_filename=args.input,
        output_filename=args.output,
        mean=args.mean,
        sdev=args.sdev,
        vmin=args.min,
        vmax=args.max,
        scale=args.scale,
        offset=args.offset,
    )


def rotate(args):
    """
    Rotate a map by multiples of 90 about an axis

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.rotate(
        input_filename=args.input,
        output_filename=args.output,
        axes=args.axes,
        num=args.num,
    )


def segment(args):
    """
    Segment the map

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.segment(
        input_filename=args.input,
        output_filename=args.output,
        num_objects=args.num_objects,
    )


def threshold(args):
    """
    Threshold the map

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.threshold(
        input_filename=args.input,
        output_filename=args.output,
        threshold=args.threshold,
        normalize=args.normalize,
        zero=args.zero,
    )


def transform(args):
    """
    Transform the map

    Args:
        args (object): The parsed arguments

    """
    selknam.maptools.transform(
        input_filename=args.input,
        output_filename=args.output,
        offset=args.offset,
        rotation=args.rotation,
        translation=args.translation,
        deg=args.deg,
    )


def main(args=None):
    """
    Process the map

    Args:
        args (list): The command line arguments

    """

    def add_cc_arguments(subparsers, parser_common):
        """
        Add command line arguments for the cc command

        """

        # Create the parser for the "cc" command
        parser_cc = subparsers.add_parser(
            "cc", parents=[parser_common], help="Compute map CC in real space"
        )

        # Add some arguments
        parser_cc.add_argument(
            "-i2",
            "--input2",
            dest="input2",
            type=str,
            default=None,
            help="The second input map file",
        )
        parser_cc.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="cc.mrc",
            help="The output map file",
        )

    def add_crop_arguments(subparsers, parser_common):
        """
        Add command line arguments for the crop command

        """

        # Create the parser for the "crop" command
        parser_crop = subparsers.add_parser(
            "crop", parents=[parser_common], help="Crop the map"
        )

        # Add some arguments
        parser_crop.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="cropped.mrc",
            help="The output map file",
        )
        parser_crop.add_argument(
            "-r",
            "--roi",
            dest="roi",
            type=lambda s: [int(x) for x in s.split(",")],
            default=None,
            help="The region of interest (z0,y0,x0,z1,y1,x1)",
        )

    def add_edit_arguments(subparsers, parser_common):
        """
        Add command line arguments for the edit command

        """

        # Create the parser for the "edit" command
        parser_edit = subparsers.add_parser(
            "edit", parents=[parser_common], help="Edit the map"
        )

        # Add some arguments
        parser_edit.add_argument(
            "--voxel_size",
            dest="voxel_size",
            type=lambda s: [int(x) for x in s.split(",")],
            default=None,
            help="The voxel size (sz, sy, sx)",
        )

    def add_fft_arguments(subparsers, parser_common):
        """
        Add command line arguments for the fft command

        """

        # Create the parser for the "fft" command
        parser_fft = subparsers.add_parser(
            "fft", parents=[parser_common], help="Compute map FFT"
        )

        # Add some arguments
        parser_fft.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="fft.mrc",
            help="The output map file",
        )
        parser_fft.add_argument(
            "-m",
            "--mode",
            dest="mode",
            type=str,
            choices=["real", "imaginary", "amplitude", "phase", "power"],
            default="power",
            help="The fft output",
        )
        parser_fft.add_argument(
            "-s",
            "--shift",
            dest="shift",
            type=bool,
            default=True,
            help="Shift the Fourier components",
        )
        parser_fft.add_argument(
            "-n",
            "--normalize",
            dest="normalize",
            type=bool,
            default=True,
            help="Normalize before computing FFT",
        )

    def add_filter_arguments(subparsers, parser_common):
        """
        Add command line arguments for the filter command

        """

        # Create the parser for the "filter" command
        parser_filter = subparsers.add_parser(
            "filter", parents=[parser_common], help="Filter the map"
        )

        # Add some arguments
        parser_filter.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="filtered.mrc",
            help="The output map file",
        )
        parser_filter.add_argument(
            "-t",
            "--type",
            dest="type",
            type=str,
            choices=["lowpass", "highpass", "bandpass", "bandstop"],
            default="lowpass",
            help="The type of filter to use",
        )
        parser_filter.add_argument(
            "-r",
            "--resolution",
            dest="resolution",
            type=lambda s: [int(x) for x in s.split(",")],
            default=None,
            help="The resolution",
        )
        parser_filter.add_argument(
            "-s",
            "--shape",
            dest="shape",
            type=str,
            choices=["square", "gaussian"],
            default="gaussian",
            help="The shape of the filter",
        )

    def add_fit_arguments(subparsers, parser_common):
        """
        Add command line arguments for the fit command

        """

        # Create the parser for the "fft" command
        parser_fit = subparsers.add_parser(
            "fit",
            parents=[parser_common],
            help="Fit the coords into the map (requires REFMAC5)",
        )

        # Add some arguments
        parser_fit.add_argument(
            "-i2",
            "--input2",
            dest="input2",
            type=str,
            default=None,
            required=True,
            help="The input coordinate file",
        )

        # Add some arguments
        parser_fit.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="fft.mrc",
            help="The output map file",
        )
        parser_fit.add_argument(
            "-r",
            "--resolution",
            dest="resolution",
            type=float,
            default=1,
            help="The resolution",
        )
        parser_fit.add_argument(
            "-n",
            "--ncycle",
            dest="ncycle",
            type=int,
            default=10,
            help="The number of refinement cycles",
        )
        parser_fit.add_argument(
            "-m",
            "--mode",
            dest="mode",
            type=str,
            choices=["rigid_body", "jelly_body"],
            default="rigid_body",
            help="The refinement mode",
        )
        parser_fit.add_argument(
            "-l",
            "--logfile",
            dest="logfile",
            type=str,
            default="fit.log",
            help="Destination for the log file",
        )

    def add_fsc_arguments(subparsers, parser_common):
        """
        Add command line arguments for the fsc command

        """

        # Create the parser for the "fsc" command
        parser_fsc = subparsers.add_parser(
            "fsc", parents=[parser_common], help="Compute map FSC"
        )

        # Add some arguments
        parser_fsc.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="fsc.png",
            help="The output fsc curvae",
        )
        parser_fsc.add_argument(
            "-d",
            "--output_data",
            dest="output_data",
            type=str,
            default="fsc.yaml",
            help="The output file for the data table",
        )
        parser_fsc.add_argument(
            "-i2",
            "--input2",
            dest="input2",
            type=str,
            default=None,
            help="The input map file",
        )
        parser_fsc.add_argument(
            "-n",
            "--nbins",
            dest="nbins",
            type=int,
            default=20,
            help="The number of FSC bins",
        )
        parser_fsc.add_argument(
            "-r",
            "--resolution",
            dest="resolution",
            type=float,
            default=None,
            help="The resolution to compute to",
        )
        parser_fsc.add_argument(
            "--axis",
            dest="axis",
            type=lambda s: [int(x) for x in s.split(",")],
            default=None,
            help="The axes in which to compute the FSC",
        )
        parser_fsc.add_argument(
            "-m",
            "--method",
            dest="method",
            type=str,
            default="binned",
            choices=["binned", "averaged"],
            help="The method to use to calculate FSC",
        )

    def add_fsc3d_arguments(subparsers, parser_common):
        """
        Add command line arguments for the fsc3d command

        """

        # Create the parser for the "fsc" command
        parser_fsc3d = subparsers.add_parser(
            "fsc3d", parents=[parser_common], help="Compute local map FSC"
        )

        # Add some arguments
        parser_fsc3d.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="fsc.mrc",
            help="The output local map fsc file",
        )
        parser_fsc3d.add_argument(
            "-i2",
            "--input2",
            dest="input2",
            type=str,
            default=None,
            help="The input map file",
        )
        parser_fsc3d.add_argument(
            "-k",
            "--kernel",
            dest="kernel",
            type=int,
            default=9,
            help="The kernel to compute the local FSC",
        )

        # Add some arguments
        parser_fsc3d.add_argument(
            "-r",
            "--resolution",
            dest="resolution",
            type=float,
            default=None,
            help="The resolution to compute to",
        )

    def add_mask_arguments(subparsers, parser_common):
        """
        Add command line arguments for the mask command

        """

        # Create the parser for the "mask" command
        parser_mask = subparsers.add_parser(
            "mask", parents=[parser_common], help="Mask the map"
        )

        # Add some arguments
        parser_mask.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="masked.mrc",
            help="The output map file",
        )
        parser_mask.add_argument(
            "-m",
            "--mask",
            dest="mask",
            type=str,
            default=None,
            required=True,
            help="The input mask file",
        )
        parser_mask.add_argument(
            "-f",
            "--fourier_space",
            dest="fourier_space",
            type=bool,
            default=False,
            help="Apply the mask in Fourier space",
        )
        parser_mask.add_argument(
            "-s",
            "--shift",
            dest="shift",
            type=bool,
            default=False,
            help="Shift the mask",
        )

    def add_map2mtz_arguments(subparsers, parser_common):
        """
        Add command line arguments for the reorder map2mtz command

        """

        # Create the parser for the "reorder" command
        parser_map2mtz = subparsers.add_parser(
            "map2mtz",
            parents=[parser_common],
            help="Convert the map to an mtz file (requires REFMAC5)",
        )

        # Add some arguments
        parser_map2mtz.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="hklout.mtz",
            help="The output mtz file",
        )
        parser_map2mtz.add_argument(
            "-r",
            "--resolution",
            dest="resolution",
            type=float,
            default=1,
            help="The resolution",
        )

    def add_pdb2map_arguments(subparsers, parser_common):
        """
        Add command line arguments for the reorder pdb2map command

        """

        # Create the parser for the "reorder" command
        parser_pdb2map = subparsers.add_parser(
            "pdb2map",
            parents=[parser_common],
            help="Convert the pdb to map file (requires REFMAC5 and FFT)",
        )

        # Add some arguments
        parser_pdb2map.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="output.mrc",
            help="The output map file",
        )
        parser_pdb2map.add_argument(
            "-r",
            "--resolution",
            dest="resolution",
            type=float,
            default=None,
            help="The resolution",
        )
        parser_pdb2map.add_argument(
            "-g",
            "--grid",
            dest="grid",
            type=lambda s: [int(x) for x in s.split(",")],
            default=None,
            help="The grid",
        )

    def add_reorder_arguments(subparsers, parser_common):
        """
        Add command line arguments for the reorder command

        """

        # Create the parser for the "reorder" command
        parser_reorder = subparsers.add_parser(
            "reorder", parents=[parser_common], help="Reorder the map axes"
        )

        # Add some arguments
        parser_reorder.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="reordered.mrc",
            help="The output map file",
        )
        parser_reorder.add_argument(
            "-a",
            "--axis_order",
            dest="axis_order",
            type=lambda s: [int(x) for x in s.split(",")],
            default=None,
            help="The axis order",
        )

    def add_rebin_arguments(subparsers, parser_common):
        """
        Add command line arguments for the rebin command

        """

        # Create the parser for the "rebin" command
        parser_rebin = subparsers.add_parser(
            "rebin", parents=[parser_common], help="Resample the map"
        )

        # Add some arguments
        parser_rebin.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="rebind.mrc",
            help="The output map file",
        )
        parser_rebin.add_argument(
            "-s",
            "--shape",
            dest="shape",
            type=lambda s: [int(x) for x in s.split(",")],
            default=None,
            help="The new shape",
        )

    def add_rescale_arguments(subparsers, parser_common):
        """
        Add command line arguments for the rescale command

        """

        # Create the parser for the "threshold" command
        parser_rescale = subparsers.add_parser(
            "rescale", parents=[parser_common], help="Rescale the map"
        )

        # Add some arguments
        parser_rescale.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="rescaled.mrc",
            help="The output map file",
        )
        parser_rescale.add_argument(
            "--mean", dest="mean", type=float, default=None, help="The mean",
        )
        parser_rescale.add_argument(
            "--sdev",
            dest="sdev",
            type=float,
            default=None,
            help="The standard deviation",
        )
        parser_rescale.add_argument(
            "--min", dest="min", type=float, default=None, help="The minimum",
        )
        parser_rescale.add_argument(
            "--max", dest="max", type=float, default=None, help="The maximum",
        )
        parser_rescale.add_argument(
            "--scale", dest="scale", type=float, default=None, help="The scale",
        )
        parser_rescale.add_argument(
            "--offset", dest="offset", type=float, default=None, help="The offset",
        )

    def add_rotate_arguments(subparsers, parser_common):
        """
        Add command line arguments for the rotate command

        """

        # Create the parser for the "rotate" command
        parser_rotate = subparsers.add_parser(
            "rotate",
            parents=[parser_common],
            help="Rotate the map by 90 degrees along an axis",
        )

        # Add some arguments
        parser_rotate.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="rotated.mrc",
            help="The output map file",
        )
        parser_rotate.add_argument(
            "-a",
            "--axes",
            dest="axes",
            type=lambda s: [int(x) for x in s.split(",")],
            default=(0, 1),
            help="The axes",
        )
        parser_rotate.add_argument(
            "-n",
            "--num",
            dest="num",
            type=int,
            default=1,
            help="The number of times to rotate by 90 degrees",
        )

    def add_segment_arguments(subparsers, parser_common):
        """
        Add command line arguments for the segment command

        """

        # Create the parser for the "segment" command
        parser_segment = subparsers.add_parser(
            "segment", parents=[parser_common], help="Threshold the map"
        )

        # Add some arguments
        parser_segment.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="segmented.mrc",
            help="The output map file",
        )
        parser_segment.add_argument(
            "-n",
            "--num_objects",
            dest="num_objects",
            type=int,
            default=1,
            help="The number of objects",
        )

    def add_threshold_arguments(subparsers, parser_common):
        """
        Add command line arguments for the threshold command

        """

        # Create the parser for the "threshold" command
        parser_threshold = subparsers.add_parser(
            "threshold", parents=[parser_common], help="Threshold the map"
        )

        # Add some arguments
        parser_threshold.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="thresholded.mrc",
            help="The output map file",
        )
        parser_threshold.add_argument(
            "-t",
            "--threshold",
            dest="threshold",
            type=float,
            default=0,
            help="The threshold",
        )
        parser_threshold.add_argument(
            "-n",
            "--normalize",
            dest="normalize",
            type=bool,
            default=False,
            help="Normalize the data before thresholding",
        )
        parser_threshold.add_argument(
            "-z",
            "--zero",
            dest="zero",
            type=bool,
            default=True,
            help="Zero the thresholded data",
        )

    def add_transform_arguments(subparsers, parser_common):
        """
        Add command line arguments for the transform command

        """

        # Create the parser for the "transform" command
        parser_transform = subparsers.add_parser(
            "transform", parents=[parser_common], help="Transform the map"
        )

        # Add some arguments
        parser_transform.add_argument(
            "-o",
            "--output",
            dest="output",
            type=str,
            default="transformed.mrc",
            help="The output map file",
        )
        parser_transform.add_argument(
            "-a",
            "--offset",
            dest="offset",
            type=str,
            default=None,
            help="The offset (default is the centre of the map)",
        )
        parser_transform.add_argument(
            "-r",
            "--rotation",
            dest="rotation",
            type=lambda s: [float(x) for x in s.split(",")],
            default=(0, 0, 0),
            help="The rotation",
        )
        parser_transform.add_argument(
            "-t",
            "--translation",
            dest="translation",
            type=lambda s: [float(x) for x in s.split(",")],
            default=(0, 0, 0),
            help="The translation",
        )
        parser_transform.add_argument(
            "-d",
            "--deg",
            dest="deg",
            type=bool,
            default=True,
            help="Is the rotation in degrees",
        )

    # Create a parser for common args
    parser_common = argparse.ArgumentParser(add_help=False)

    # Common arguments
    parser_common.add_argument(
        "-i",
        "--input",
        dest="input",
        type=str,
        default=None,
        required=True,
        help="The input map file",
    )
    parser_common.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Set verbose output",
    )

    # The command line parser
    parser = argparse.ArgumentParser(
        prog="map", description="A tool to process CryoEM maps"
    )

    # Create the subparsers
    subparsers = parser.add_subparsers(dest="command", help="The sub commands")

    # Add arguments for the sub commands
    add_cc_arguments(subparsers, parser_common)
    add_crop_arguments(subparsers, parser_common)
    add_edit_arguments(subparsers, parser_common)
    add_fft_arguments(subparsers, parser_common)
    add_filter_arguments(subparsers, parser_common)
    add_fit_arguments(subparsers, parser_common)
    add_fsc_arguments(subparsers, parser_common)
    add_fsc3d_arguments(subparsers, parser_common)
    add_mask_arguments(subparsers, parser_common)
    add_reorder_arguments(subparsers, parser_common)
    add_rebin_arguments(subparsers, parser_common)
    add_rescale_arguments(subparsers, parser_common)
    add_rotate_arguments(subparsers, parser_common)
    add_segment_arguments(subparsers, parser_common)
    add_threshold_arguments(subparsers, parser_common)
    add_transform_arguments(subparsers, parser_common)
    add_map2mtz_arguments(subparsers, parser_common)
    add_pdb2map_arguments(subparsers, parser_common)

    # Parse some argument lists
    args = parser.parse_args(args=args)
    if args.command is None:
        parser.print_help()
        return

    # Set the logger
    if args.verbose is True:
        level = logging.INFO
    else:
        level = logging.WARN
    logging.basicConfig(level=level, format="%(msg)s")

    # Call the appropriate function
    {
        "cc": cc,
        "crop": crop,
        "edit": edit,
        "fft": fft,
        "filter": filter,
        "fit": fit,
        "fsc": fsc,
        "fsc3d": fsc3d,
        "map2mtz": map2mtz,
        "mask": mask,
        "pdb2map": pdb2map,
        "reorder": reorder,
        "segment": segment,
        "threshold": threshold,
        "rebin": rebin,
        "rescale": rescale,
        "rotate": rotate,
        "transform": transform,
    }[args.command](args)
