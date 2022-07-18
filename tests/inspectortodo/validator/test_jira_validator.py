# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

from unittest.mock import Mock

from inspectortodo.todo import Todo
from inspectortodo.validator import JiraValidator


class JiraValidatorForTesting(JiraValidator):

    def __init__(self, issue_pattern, allowed_statuses, issue_filter_field=None, issue_filter_values=None):
        super().__init__(issue_pattern, '', '', '', allowed_statuses, issue_filter_field, issue_filter_values)
        self.issues = {}

    def _init_jira_client(self, url, username, password):
        pass

    def _fetch_issue(self, issue_id):
        return self.issues[issue_id]


PATTERN = r'SP-\d+'
VALID_STATUS = 'Valid Status'
INVALID_STATUS = 'Invalid Status'
FILTER_FIELD = 'filter_key'
FITTING_FILTER_VALUE = 'Fitting Filter Value'
UNFITTING_FILTER_VALUE = 'Unfitting Filter Value'


def test_valid_status():
    issue_id = 'SP-4711'
    issue = _initialize_issue_with_status(VALID_STATUS, None)

    todo = Todo('some path', 23, 'TODO ' + issue_id + ': content containing valid issue reference')

    validator = JiraValidatorForTesting(PATTERN, [VALID_STATUS])
    validator.issues[issue_id] = issue
    validator.validate(todo)

    assert todo.is_valid is True


def test_invalid_status():
    issue_id = 'SP-4711'
    issue = _initialize_issue_with_status(INVALID_STATUS, None)

    todo = Todo('some path', 23, 'TODO ' + issue_id + ': content containing valid issue reference')

    validator = JiraValidatorForTesting(PATTERN, [VALID_STATUS])
    validator.issues[issue_id] = issue
    validator.validate(todo)

    assert todo.is_valid is False


def test_invalid_status_valid_parent_status():
    parent_issue_id = 'SP-0815'
    parent_issue = _initialize_issue_with_status(VALID_STATUS, None)
    issue_id = 'SP-4711'
    issue = _initialize_issue_with_status(INVALID_STATUS, parent_issue_id)

    todo = Todo('some path', 23, 'TODO ' + issue_id + ': content containing valid issue reference')

    validator = JiraValidatorForTesting(PATTERN, [VALID_STATUS])
    validator.issues[issue_id] = issue
    validator.issues[parent_issue_id] = parent_issue
    validator.validate(todo)

    assert todo.is_valid is True


def test_invalid_status_invalid_parent_status():
    parent_issue_id = 'SP-0815'
    parent_issue = _initialize_issue_with_status(INVALID_STATUS, None)
    issue_id = 'SP-4711'
    issue = _initialize_issue_with_status(INVALID_STATUS, parent_issue_id)

    todo = Todo('some path', 23, 'TODO ' + issue_id + ': content containing valid issue reference')

    validator = JiraValidatorForTesting(PATTERN, [VALID_STATUS])
    validator.issues[issue_id] = issue
    validator.issues[parent_issue_id] = parent_issue
    validator.validate(todo)

    assert todo.is_valid is False


def test_invalid_status_fitting_filter_then_todo_marked_invalid():
    issue_id = 'SP-4711'
    issue = _initialize_issue_with_status(INVALID_STATUS, None, filter_key=FILTER_FIELD, filter_value=FITTING_FILTER_VALUE)

    todo = Todo('some path', 23, 'TODO ' + issue_id + ': content containing valid issue reference')

    validator = JiraValidatorForTesting(PATTERN, [VALID_STATUS], issue_filter_field=FILTER_FIELD, issue_filter_values=[FITTING_FILTER_VALUE])
    validator.issues[issue_id] = issue
    validator.validate(todo)

    assert todo.is_valid is False


def test_invalid_status_unfitting_filter_then_todo_marked_valid():
    issue_id = 'SP-4711'
    issue = _initialize_issue_with_status(INVALID_STATUS, None, filter_key=FILTER_FIELD, filter_value=UNFITTING_FILTER_VALUE)

    todo = Todo('some path', 23, 'TODO ' + issue_id + ': content containing valid issue reference')

    validator = JiraValidatorForTesting(PATTERN, [VALID_STATUS], issue_filter_field=FILTER_FIELD, issue_filter_values=[FITTING_FILTER_VALUE])
    validator.issues[issue_id] = issue
    validator.validate(todo)

    assert todo.is_valid is True


def test_invalid_status_filter_key_not_present_in_issue_then_todo_marked_valid():
    issue_id = 'SP-4711'
    issue = _initialize_issue_with_status(INVALID_STATUS, None, filter_key=None, filter_value=None)

    todo = Todo('some path', 23, 'TODO ' + issue_id + ': content containing valid issue reference')

    validator = JiraValidatorForTesting(PATTERN, [VALID_STATUS], issue_filter_field=FILTER_FIELD, issue_filter_values=[FITTING_FILTER_VALUE])
    validator.issues[issue_id] = issue
    validator.validate(todo)

    assert todo.is_valid is True


def test_invalid_status_filter_key_present_in_issue_but_value_none_then_todo_marked_valid():
    issue_id = 'SP-4711'
    issue = _initialize_issue_with_status(INVALID_STATUS, None, filter_key=FILTER_FIELD, filter_value=None)

    todo = Todo('some path', 23, 'TODO ' + issue_id + ': content containing valid issue reference')

    validator = JiraValidatorForTesting(PATTERN, [VALID_STATUS], issue_filter_field=FILTER_FIELD, issue_filter_values=[FITTING_FILTER_VALUE])
    validator.issues[issue_id] = issue
    validator.validate(todo)

    assert todo.is_valid is True


def test_invalid_status_fitting_filter_in_list_then_todo_marked_invalid():
    issue_id = 'SP-4711'
    issue = _initialize_issue_with_status(INVALID_STATUS, None, filter_key=FILTER_FIELD, filter_value=[FITTING_FILTER_VALUE, UNFITTING_FILTER_VALUE])

    todo = Todo('some path', 23, 'TODO ' + issue_id + ': content containing valid issue reference')

    validator = JiraValidatorForTesting(PATTERN, [VALID_STATUS], issue_filter_field=FILTER_FIELD, issue_filter_values=[FITTING_FILTER_VALUE])
    validator.issues[issue_id] = issue
    validator.validate(todo)

    assert todo.is_valid is False


def _initialize_issue_with_status(status, parent_id, filter_key=None, filter_value=None):
    issue = Mock()
    issue.fields = Mock()
    issue.fields.status = status
    issue.fields.parent = parent_id
    issue.raw = {'fields': {}}
    if filter_key:
        issue.raw['fields'] = {filter_key: filter_value}
    return issue
