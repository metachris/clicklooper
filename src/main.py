#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Documentation here

Link to project: YOUR_PROJECT_LINK

Copyright (c) 2015, YOUR_NAME
License: YOUR_LICENSE
"""
import sys

__title__ = 'MousePlayer'
__version__ = '1.0.0'
__author__ = 'Chris Hager'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2015 Chris Hager'

# Regular imports
import argparse
from player import MediaPlayer
from logutils import setup_logger

logger = setup_logger()


def main(basedir):
    player = MediaPlayer(basedir)
    player.start()


if __name__ == "__main__":
    """
    This is executed when run from the command line
    """
    parser = argparse.ArgumentParser(
            description='Command description to show on -v',
            # epilog="Text after command help"
    )

    parser.add_argument("directory", help="Base directory")
    # parser.add_argument('-v', '--verbose', action='count', default=0, help="Verbosity (-v, -vv, etc)")
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s (version {version})'.format(version=__version__))
    args = parser.parse_args()

    main(args.directory)
