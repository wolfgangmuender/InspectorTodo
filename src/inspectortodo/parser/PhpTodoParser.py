# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

from .BaseTodoParser import BaseTodoParser


class PhpTodoParser(BaseTodoParser):
    def __init__(self, keywords):
        super().__init__('//', '/*', '*/', keywords)
