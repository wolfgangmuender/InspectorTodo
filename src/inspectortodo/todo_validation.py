import logging

from .config import get_config_value, get_config_value_as_list
from .validator import (JiraValidator, RegExpValidator, VersionsValidator)

log = logging.getLogger()


def validate_todos(todos, issue_pattern, version_pattern, version, versions):
    log.info('Validating %d todos.', len(todos))

    validators = []

    issue_validator = RegExpValidator(issue_pattern)
    validators.append(issue_validator)

    if get_config_value('jira_server', 'url'):
        jira_validator = JiraValidator(issue_pattern,
                                       get_config_value('jira_server', 'url'),
                                       get_config_value('jira_server', 'username'),
                                       get_config_value('jira_server', 'password'),
                                       get_config_value('jira_server', 'token'),
                                       get_config_value_as_list('statuses', 'all'),
                                       get_config_value('issue_filter', 'field'),
                                       get_config_value_as_list('issue_filter', 'values'))
        issue_validator.set_dependent_validator(jira_validator)

    if version_pattern is not None:
        version_validator = RegExpValidator(version_pattern)
        validators.append(version_validator)

        if versions is not None and version is not None:
            version_validator.set_dependent_validator(VersionsValidator(versions, version))

    invalid_todos = []
    amount_ignored = 0
    for todo in todos:
        validate_todo(validators, todo)
        if not todo.is_valid:
            invalid_todos.append(todo)
            amount_ignored += todo.is_ignored

    if not invalid_todos:
        log.info('All todos are fine.')
        return

    log.error('------------------------------------------------------------------------------')
    log.error('Found %d invalid todo(s) (%d of them ignored).', len(invalid_todos), amount_ignored)
    log.error('------------------------------------------------------------------------------')
    for invalid_todo in invalid_todos:
        invalid_todo.print()
        log.error('------------------------------------------------------------------------------')


def validate_todo(validators, todo):
    for validator in validators:
        if validator.validate(todo):
            return

    todo.mark_as_invalid('Todo is not conform to any validator.')
