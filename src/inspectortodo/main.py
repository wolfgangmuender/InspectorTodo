# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import logging
import os

import click
import click_log

from .find_invalid_todos import find_invalid_todos


click_log.basic_config()


@click.command()
@click.argument('ROOT_DIR', required=True, help='Root directory to inspect.')
@click.argument('TICKET-PATTERN', required=True, help='Pattern for ticket reference in todo.')
@click.option('--version-pattern', help='Pattern for version reference in todo.')
@click.option('--version', help='Current version.')
@click.option('--versions', nargs='*', help='List of versions allowed in todos. Versions increase from left to right.')
@click.option('--log-level', default='INFO', help="Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
def main(root_dir, ticket_pattern, version_pattern, version, versions, log_level):

    logging.basicConfig(level=log_level.upper(), format='[%(levelname)s] %(message)s')

    root_dir = os.path.normpath(os.path.abspath(root_dir))

    find_invalid_todos(root_dir, ticket_pattern, version_pattern, version, versions)
