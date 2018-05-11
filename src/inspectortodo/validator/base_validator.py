# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory


class BaseValidator:

    def __init__(self):
        self._dependent_validator = None

    def set_dependent_validator(self, dependent_validator):
        self._dependent_validator = dependent_validator
        pass

    def validate(self, todo):
        is_valid = self._validate(todo)

        if is_valid and self._dependent_validator:
            self._dependent_validator.validate(todo)

        return is_valid

    def _validate(self, todo):
        raise Exception("Override this method in specific validators.")
