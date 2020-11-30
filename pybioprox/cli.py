"""cli.py

Command Line Interface for pybioprox

J. Metz <metz.jp@gmail.com>
"""

import argparse
import pybioprox.main as main


def create_parser():
    """
    Create the parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Folder to process")
    parser.add_argument("--output-folder", help="Output folder")
    # parser.add_argument(
    #    "-v", "--verbose", help="Increase output verbosity",
    #    action="store_true")
    # parser.add_argument("-d", type=int, choices=[0, 1, 2],
    #                    help="Choices...")
    return parser


def run():
    """
    Main CLI run function

    Creates an appropriate ArgumentParser and parses the command
    line arguments, passing parameters through to pybioprox.main.main
    """
    parser = create_parser()
    args = parser.parse_args()

    main.main(args.folder, output_folder=args.output_folder)
