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

    if version_pattern is not None:
        version_validator = RegExpValidator(version_pattern)
        if versions is not None and version is not None:
            version_validator.set_dependent_validator(VersionsValidator(versions, version))
        validators.append(version_validator)

    invalid_todos = []
    for todo in todos:
        validate_todo(validators, todo)
        if not todo.is_valid:
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


def validate_todo(validators, todo):
    for validator in validators:
        if validator.validate(todo):
            return

    todo.mark_as_invalid('Todo is not conform to any validator!')
