# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import logging

from .validator import (RegExpValidator, VersionsValidator)


log = logging.getLogger()


def validate_todos(todos, ticket_pattern, version_pattern, version, versions):
    log.info('Validating %d todos.', len(todos))

    validators = [
        RegExpValidator(ticket_pattern)
    ]
    if versions is not None and version is not None:
        validators += VersionsValidator(versions, version)
    if version_pattern is not None:
        validators += RegExpValidator(version_pattern)

    invalid_todos = []
    for todo in todos:
        for validator in validators:
            if validator.validate(todo):
                continue

        todo.mark_as_invalid('Todo is not conform to any validator!')
        invalid_todos.append(todo)

    if not invalid_todos:
        log.info('All todos are fine.')
        return

    log.error('------------------------------------------------------------------------------')
    log.error('Found {} invalid todos.'.format(len(invalid_todos)))
    log.error('------------------------------------------------------------------------------')
    for invalid_todo in invalid_todos:
        invalid_todo.print()
        log.error('------------------------------------------------------------------------------')
