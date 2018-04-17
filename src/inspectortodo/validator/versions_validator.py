# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory


class VersionsValidator:

    def __init__(self, versions, current_version=None):
        if current_version in versions:
            self.allowed_versions = versions[versions.index(current_version)+1:]
        else:
            self.allowed_versions = versions

    def validate(self, todo):
        for version in self.allowed_versions:
            if version in todo.content:
                return True
        return False
