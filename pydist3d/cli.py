"""cli.py

Command Line Interface for pydist3d

J. Metz <metz.jp@gmail.com>
"""

import argparse
import pydist3d.main as main


def create_parser():
    """
    Create the parser
    """
    parser = argparse.ArgumentParser()
    # TODO: Select inputs - see below
    # parser.add_argument("num", help="A positional input")
    # parser.add_argument(
    #    "-v", "--verbose", help="Increase output verbosity",
    #    action="store_true")
    # parser.add_argument("-d", type=int, choices=[0, 1, 2],
    #                    help="Choices...")
    return parser


def run():
    parser = create_parser()
    args = parser.parse_args()

    # TODO: Pass args into main?
    main.main()
