import re

from .base_validator import BaseValidator


class RegExpValidator(BaseValidator):

    def __init__(self, regexp):
        super().__init__()
        self.regexp = regexp
        self.regexp_compiled = re.compile(regexp)

    def _validate(self, todo):
        match = self.regexp_compiled.search(todo.content)
        if match:
            todo.mark_as_valid()
            return True
        else:
            todo.mark_as_invalid('Todo does not match regular expression \'{}\'.'.format(self.regexp))
            return False
