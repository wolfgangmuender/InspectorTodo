from .base_validator import BaseValidator


class VersionsValidator(BaseValidator):

    def __init__(self, versions, current_version=None):
        super().__init__()
        if current_version in versions:
            self.allowed_versions = versions[versions.index(current_version)+1:]
        else:
            self.allowed_versions = versions

    def _validate(self, todo):
        for version in self.allowed_versions:
            if version in todo.content:
                todo.mark_as_valid()
                return True

        todo.mark_as_invalid('Todo does not refer to an allowed version.')
        return False
