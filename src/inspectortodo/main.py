import logging
import os

import click

from .config import load_or_create_configfile, get_config_value, get_multiline_config_value_as_list, set_config_value
from .todo_finder import TodoFinder
from .todo_validation import validate_todos

log = logging.getLogger()


@click.command()
@click.argument('ROOT_DIR', required=True)
@click.argument('ISSUE_PATTERN', required=True)
@click.option('--version-pattern', help='Regular expression for version references in todos.')
@click.option('--version', help='Current version.')
@click.option('--versions', help='List of versions allowed in todos.'
                                 'Versions are separated by comma and increase from left to right.')
@click.option('--configfile', help='Config file to be used. If file does not exist, default config is created.'
                                   'If not set, all config values are treated as None.')
@click.option('--jira-user', help="Jira username")
@click.option('--jira-password', help="Jira password")
@click.option('--jira-token', help="Jira API Token")
@click.option('--issue-filter-field', help="Issue field to filter for, when checking ToDos")
@click.option('--issue-filter-values', help="Values that are checked against the field determined by"
                                            " --`issue-filter-field`. If it matches any of the values here, the ToDo is"
                                            " included in the final report")
@click.option('--xml', help="Output file for JUnit like xml which contains all found todos.")
@click.option('--log-level', default='INFO', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']),
              help="Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
def main(root_dir, issue_pattern, version_pattern, version, versions, configfile, jira_user, jira_password, jira_token,
         issue_filter_field, issue_filter_values, xml, log_level):
    r"""
    ROOT_DIR is the directory to inspect recursively.

    ISSUE_PATTERN is a regular expression for issue references in todos. The regular expression has to match the entire
    issue reference, e.g. IT-\d+
    """

    logging.basicConfig(level=log_level.upper(), format='[%(levelname)s] %(message)s')

    root_dir = os.path.normpath(os.path.abspath(root_dir))
    issue_pattern = issue_pattern.strip()
    versions = versions.split(',') if versions else versions

    if configfile:
        load_or_create_configfile(configfile)
    if jira_user:
        set_config_value('jira_server', 'username', jira_user)
    if jira_password:
        set_config_value('jira_server', 'password', jira_password)
    if jira_token:
        set_config_value('jira_server', 'token', jira_token)
    if issue_filter_field and issue_filter_values:
        set_config_value('issue_filter', 'field', issue_filter_field)
        set_config_value('issue_filter', 'values', issue_filter_values)

    paths_ignore_list = []
    if get_config_value('paths', 'ignore_list'):
        paths_ignore_list = get_multiline_config_value_as_list('paths', 'ignore_list')
    # stay backwards compatible for a while
    if get_config_value('files', 'whitelist'):
        paths_ignore_list = get_multiline_config_value_as_list('files', 'whitelist')

    todo_finder = TodoFinder(root_dir, paths_ignore_list)
    todos = todo_finder.find()

    if todos:
        validate_todos(todos, issue_pattern, version_pattern, version, versions)

    if xml:
        write_xml_file(xml, todos)


def write_xml_file(filename, todos):
    with open(filename, 'w', encoding='UTF-8') as xml_file:
        print_xml(xml_file, todos)


def print_xml(xml_file, todos):
    num_failed = len([todo for todo in todos if not todo.is_valid])

    xml_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    xml_file.write('<testsuite name="InspectorTodo" tests="{}" failures="{}">\n'.format(len(todos), num_failed))
    for todo in todos:
        todo.print_xml(xml_file)
    xml_file.write('</testsuite>\n')
