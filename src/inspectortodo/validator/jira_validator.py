# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import logging
import re

from jira import JIRA

from .base_validator import BaseValidator

log = logging.getLogger()


class JiraValidator(BaseValidator):

    def __init__(self, issue_pattern, url, username, password, allowed_statuses):
        super().__init__()
        self.issue_pattern = issue_pattern
        self.issue_pattern_compiled = re.compile(issue_pattern)
        self.allowed_statuses = allowed_statuses

        self._init_jira_client(url, username, password)

    def _init_jira_client(self, url, username, password):
        self._jira_client = JIRA(url, auth=(username, password))

    def _validate(self, todo):
        match = self.issue_pattern_compiled.search(todo.content)
        if match is None:
            raise Exception('Ensure presence of ticket reference with RegExpValidator before using JiraValidator!')

        issue_id = match.group()
        issue = self._fetch_issue(issue_id)
        if not issue:
            todo.mark_as_invalid('Issue {} does not exist.'.format(issue_id))
            return False

        status = str(issue.fields.status)
        if status in self.allowed_statuses:
            todo.mark_as_valid()
            return True
        elif hasattr(issue.fields, 'parent') and issue.fields.parent:
            parent = self._fetch_issue(str(issue.fields.parent))
            parent_status = str(parent.fields.status)
            if parent_status in self.allowed_statuses:
                todo.mark_as_valid()
                return True

        todo.mark_as_invalid('Issue status is \'' + status + '\', must be one of: '
                             + ", ".join(self.allowed_statuses))
        return False

    def _fetch_issue(self, issue_id):
        log.info("Fetching issue %s", issue_id)
        return self._jira_client.issue(issue_id)
