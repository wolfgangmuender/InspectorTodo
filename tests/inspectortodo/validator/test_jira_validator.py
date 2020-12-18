# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

from unittest.mock import Mock

from inspectortodo.todo import Todo
from inspectortodo.validator import JiraValidator


class JiraValidatorForTesting(JiraValidator):

    def __init__(self, issue_pattern, allowed_statuses, report_fields):
        super().__init__(issue_pattern, '', '', '', allowed_statuses, report_fields)
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

    validator = JiraValidatorForTesting(pattern, [status], [])
    validator.issues[issue_id] = issue
    validator.validate(todo)

    assert todo.is_valid is True


def test_invalid_status():
    issue_id = 'SP-4711'
    pattern = r'SP-\d+'
    status = 'Closed'
    report_fields = ['customfield_11300']

    todo = Todo('some path', 23, 'TODO ' + issue_id + ': content containing invalid issue reference')
    issue = _initialize_issue_with_status(status)

    validator = JiraValidatorForTesting(pattern, ['In Progress'], report_fields)
    validator.issues[issue_id] = issue
    validator.validate(todo)

    assert todo.is_valid is False
    assert todo.error_reason.find("Team:['Cueball']") > 0

def _initialize_issue_with_status(status):
    issue = Mock()
    result = {'reporter.displayName': 'John Doe', 'status': status, 'customfield_11300': ['Cueball']}
    names = {'customfield_11300': 'Team'}
    issue.raw = {'fields': result, 'names': names}

    return issue
