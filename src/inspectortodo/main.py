# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import argparse
import logging
import os

from .find_invalid_todos import find_invalid_todos


log = logging.getLogger()


def main():
    parser = argparse.ArgumentParser(description=''' Searches for todos in given folder tree and complains about invalid todos. ''')
    parser.add_argument('--root-dir', required=True, metavar='DIR', help='Root directory for folder tree.')
    parser.add_argument('--ticket-pattern', required=True, help='Pattern for ticket reference in todo.')
    parser.add_argument('--version-pattern', help='Pattern for version reference in todo.')
    parser.add_argument('--version', help='Current version.')
    parser.add_argument('--versions', nargs='*', help='List of versions allowed in todos. Versions increase from left to right.')
    parser.add_argument('--log-level', metavar='LEVEL', default='INFO', help="Set the log level (WARN, DEBUG, ERROR, ...)")
    parser.add_argument('--log-file', metavar='FILE', help="Set the log file (defaults to STDERR)")
    parser.add_argument('--log-format', metavar='FORMAT', default='[%(levelname)s] %(message)s', help="Set a custom format for log messages")
    arguments = parser.parse_args()

    logging.basicConfig(filename=arguments.log_file, level=arguments.log_level.upper(), format=arguments.log_format)

    root_dir = os.path.normpath(os.path.abspath(arguments.root_dir))

    find_invalid_todos(root_dir, arguments)
