# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import logging
import os

import click

from .todo_finder import TodoFinder
from .todo_validation import validate_todos

log = logging.getLogger()


@click.command()
@click.argument('ROOT_DIR', required=True)
@click.argument('TICKET_PATTERN', required=True)
@click.option('--version-pattern', help='Regular expression for version references in todos.')
@click.option('--version', help='Current version.')
@click.option('--versions', help='List of versions allowed in todos. Versions are separated by comma and increase from left to right.')
@click.option('--log-level', default='INFO', help="Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
def main(root_dir, ticket_pattern, version_pattern, version, versions, log_level):
    """
    ROOT_DIR is the directory to inspect recursively.

    TICKET_PATTERN is a regular expression for the ticket references in todos.
    """

    logging.basicConfig(level=log_level.upper(), format='[%(levelname)s] %(message)s')

    root_dir = os.path.normpath(os.path.abspath(root_dir))
    ticket_pattern = ticket_pattern.strip()
    versions = versions.split(',') if versions else versions

    todo_finder = TodoFinder(root_dir)
    todos = todo_finder.find()
    if not todos:
        log.info('No todos found.')
        return

    validate_todos(todos, ticket_pattern, version_pattern, version, versions)
