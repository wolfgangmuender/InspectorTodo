# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import re


class RegExpValidator:

    def __init__(self, regexp):
        self.regexp = regexp
        self.regexp_compiled = re.compile(regexp)

    def validate(self, todo):
        match = self.regexp_compiled.search(todo.content)
        return match is not None
