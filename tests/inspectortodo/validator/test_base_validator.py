# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import pytest

from inspectortodo.todo import Todo
from inspectortodo.validator.base_validator import BaseValidator


class ValidatorForTesting(BaseValidator):

    def __init__(self, is_valid):
        super().__init__()
        self.is_valid = is_valid

    def _validate(self, todo):
        return self.is_valid


class RaisingValidatorException(Exception):
    pass


class RaisingValidator(BaseValidator):

    def _validate(self, todo):
        raise RaisingValidatorException()


def test_dependent_validator_is_evaluated():
    validator = ValidatorForTesting(True)
    dependent_validator = RaisingValidator()
    validator.set_dependent_validator(dependent_validator)
    with pytest.raises(RaisingValidatorException):
        validator.validate(Todo('', 0, ''))


def test_dependent_validator_is_not_evaluated_when_first_validator_not_valid():
    validator = ValidatorForTesting(False)
    dependent_validator = RaisingValidator()
    validator.set_dependent_validator(dependent_validator)
    assert not validator.validate(Todo('', 0, ''))


def test_dependent_validator_does_not_change_the_validity_of_the_validator():
    validator = ValidatorForTesting(True)
    dependent_validator = ValidatorForTesting(False)
    validator.set_dependent_validator(dependent_validator)
    assert validator.validate(Todo('', 0, ''))
