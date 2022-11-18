import logging
import re

from jira import JIRA

from .base_validator import BaseValidator

log = logging.getLogger()


class JiraValidator(BaseValidator):

    def __init__(self, issue_pattern, url, username, password, token, allowed_statuses, issue_filter_field, issue_filter_values):
        super().__init__()
        self.issue_pattern = issue_pattern
        self.issue_pattern_compiled = re.compile(issue_pattern)
        self.allowed_statuses = allowed_statuses
        self.issue_filter_field = issue_filter_field
        self.issue_filter_values = issue_filter_values

        self._init_jira_client(url, username, password, token)

    def _init_jira_client(self, url, username, password, token):
        if token:
          headers = JIRA.DEFAULT_OPTIONS["headers"].copy()
          headers["Authorization"] = "Bearer " + token
          self._jira_client = JIRA(url, options={"headers": headers})
        else:
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

        if self.issue_filter_field:
            ignored_reason = self._get_reason_if_ignored(issue)
            if ignored_reason:
                todo.mark_as_ignored(ignored_reason)

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


    def _get_reason_if_ignored(self, issue):
        if self.issue_filter_field not in issue.raw['fields']:
            # Filter key not present -> maybe wrongly configured -> warn and don't ignore!
            log.warning(f"issue_filter_field={self.issue_filter_field} not found in fields!")
            return None
        if issue.raw['fields'][self.issue_filter_field] is None:
            # Filter key not present -> maybe wrongly configured -> warn and don't ignore!
            log.warning(f"No value set for issue_filter_field={self.issue_filter_field}!")
            return None
        value_to_test_raw = issue.raw['fields'][self.issue_filter_field]
        set_of_str_values_to_test = get_as_set_of_str(value_to_test_raw)
        filter_matches = set(self.issue_filter_values).intersection(set_of_str_values_to_test)
        if filter_matches:
            log.debug(f"Filter matches: {filter_matches}!")
            return None  # Filter matches, don't ignore!
        ignored_reason = f"Ignored: {self.issue_filter_field}={set_of_str_values_to_test} does not fit filter {set(self.issue_filter_values)}"
        log.debug(ignored_reason)
        return ignored_reason

    def _matches_filter(self, issue):
        if self.issue_filter_field not in issue.raw['fields']:
            log.warning(f"issue_filter_field={self.issue_filter_field} not found in fields!")
            return False
        value_to_test_raw = issue.raw['fields'][self.issue_filter_field]
        set_of_str_values_to_test = get_as_set_of_str(value_to_test_raw)
        return bool(set(self.issue_filter_values).intersection(set_of_str_values_to_test))


def get_as_set_of_str(value_to_test_raw):
    if not value_to_test_raw:
        return set()
    elif isinstance(value_to_test_raw, (list, tuple, set)):
        return {str(v) for v in value_to_test_raw}
    elif isinstance(value_to_test_raw, (str, int, float, bool)):
        return {str(value_to_test_raw)}
    else:
        raise NotImplementedError(f"Type {type(value_to_test_raw)} is currently not supported"
                                  f" (only primitive types and lists/tuples/sets of them can be used)")
