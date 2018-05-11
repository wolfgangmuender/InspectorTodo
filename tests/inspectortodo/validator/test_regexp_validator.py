# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

from inspectortodo.parser.Todo import Todo
from inspectortodo.validator import RegExpValidator


def test_validation_via_regular_expression():
    pattern = 'SP-\d+'
    valid_todo = Todo('some path', 23, 'content containing valid ticket reference SP-4711')
    invalid_todo = Todo('some path', 23, 'content containing invalid ticket reference PS-4711')

    validator = RegExpValidator(pattern)
    assert validator.validate(valid_todo)
    assert not validator.validate(invalid_todo)
