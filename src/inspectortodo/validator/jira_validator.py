# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import logging
import re

from jira import JIRA

from .base_validator import BaseValidator

log = logging.getLogger()


class JiraValidator(BaseValidator):

    def __init__(self, issue_pattern, url, username, password, allowed_statuses, report_fields, category_fields):
        super().__init__()
        self.issue_pattern = issue_pattern
        self.issue_pattern_compiled = re.compile(issue_pattern)
        self.allowed_statuses = allowed_statuses
        self.report_fields = report_fields
        self.category_fields  = category_fields

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

        status = str(issue.raw['fields']['status']['name'])
        if status in self.allowed_statuses:
            todo.mark_as_valid()
            return True
        else:
            todo.set_category("_".join(self._category_fields(issue)))
            todo.mark_as_invalid('Issue status is \'' + status + '\', must be one of: '
                                 + ", ".join(self.allowed_statuses)
                                 + ' '
                                 + ", ".join(self._report_fields(issue)))
            return False

    def _fetch_issue(self, issue_id):
        log.info("Fetching issue %s", issue_id)
        return self._jira_client.issue(issue_id, [['status'] + self.report_fields], ['names'])

    def _report_fields(self, issue):
        fields = issue.raw['fields']
        names = issue.raw['names']
        return [names[f] + ":" + self._display(fields[f]) for f in self.report_fields]

    def _category_fields(self, issue):
        fields = issue.raw['fields']
        return [self._display(fields[f]) for f in self.category_fields]

    def _display(self, field):
        if type(field) is list:
            return "_".join([self._display(subfield) for subfield in field])
        elif type(field) is dict:
            return field['name'] if 'name' in dict else ''
        elif type(field) is str:
            return field
        else:
            return str(field)
