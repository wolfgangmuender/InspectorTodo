import configparser
import logging
import sys

DEFAULT_CONFIG = '''
[jira_server]
url: https://example.local/jira
username: test
password: test

[statuses]
# mapping of issue types to allowed statuses
all: Backlog,Todo,In Progress

[paths]
# list of file or folder paths where todos are not searched or validated, relative to the root directory
# a file is ignored if it begins with any of the paths of the ignore list, e.g.
# "project_for_testing/java" ignores the folders "project_for_testing/java" and "project_for_testing/java_script"
# and all files and folders below
ignore_list=
    folder/file1.ext
    sub/sub/file2.ext
    folder2/
    folder3
'''.strip()

_config_parser = configparser.ConfigParser()

log = logging.getLogger(__name__)


def get_config_value(category, key):

    global _config_parser

    if category in _config_parser.sections() and key in _config_parser[category]:
        return _config_parser[category][key]
    return None


def get_config_value_as_list(category, key):
    value = get_config_value(category, key)
    return value.split(',') if value else value


def get_multiline_config_value_as_list(category, key):
    value = get_config_value(category, key)
    return [x.strip() for x in value.splitlines() if x] if value else value


def set_config_value(category, key, value):
    global _config_parser

    if category not in _config_parser.sections():
        _config_parser.add_section(category)
    _config_parser[category][key] = value


def load_or_create_configfile(config_path):
    global _config_parser

    found_config = bool(_config_parser.read(config_path))
    if found_config:
        log.info('Loaded config from "%s"', config_path)
    else:
        log.info('No config file at "%s"', config_path)
        create_default_configfile(config_path)
        sys.exit(0)


def create_default_configfile(config_path):
    try:
        with open(config_path, 'x', encoding='UTF-8') as config_file:
            config_file.write(DEFAULT_CONFIG)
    except FileExistsError:
        log.error('Config file "%s" already exists', config_path)
    else:
        log.info('Created config file at "%s"', config_path)
