# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

from unittest.mock import Mock

from inspectortodo.todo import Todo
from inspectortodo.validator import JiraValidator


class JiraValidatorForTesting(JiraValidator):

    def __init__(self, issue_pattern, allowed_statuses):
        super().__init__(issue_pattern, '', '', '', allowed_statuses)
        self.issues = {}

    def _init_jira_client(self, url, username, password):
        pass

    def _fetch_issue(self, issue_id):
        return self.issues[issue_id]


PATTERN = r'SP-\d+'
VALID_STATUS = 'Valid Status'
INVALID_STATUS = 'Invalid Status'


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


def _initialize_issue_with_status(status, parent_id):
    issue = Mock()
    issue.fields = Mock()
    issue.fields.status = status
    issue.fields.parent = parent_id
    return issue
