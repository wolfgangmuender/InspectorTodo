# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

from enum import Enum


class Context(Enum):
    code = 0
    single_line_comment = 1
    multi_line_comment = 2
    annotation = 3
