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


def test_valid_status():
    issue_id = 'SP-4711'
    pattern = r'SP-\d+'
    status = 'In Progress'

    todo = Todo('some path', 23, 'TODO ' + issue_id + ': content containing valid issue reference')
    issue = _initialize_issue_with_status(status)

    validator = JiraValidatorForTesting(pattern, [status])
    validator.issues[issue_id] = issue
    validator.validate(todo)

    assert todo.is_valid is True


def _initialize_issue_with_status(status):
    issue = Mock()
    issue.fields = Mock()
    issue.fields.status = status
    return issue
