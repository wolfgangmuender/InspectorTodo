# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import configparser
import logging
import sys
from collections import defaultdict

DEFAULT_CONFIG = '''
[jira_server]
url: https://example.local/jira
username: test
password: test

[statuses]
# mapping of issue types to allowed statuses
all: Backlog,Todo,In Progress

[report]
# comma separated list of extra fields to report on invalid todos
fields:

[files]
# whitelist of file or folder paths where todos are not searched or validated, relative to the root directory
# a file is whitelisted if it begins with any of the paths of the whitelist, e.g.
# "project_for_testing/java" whitelists the folders "project_for_testing/java" and "project_for_testing/java_script"
# and all files and folders below
whitelist=
    folder/file1.ext
    sub/sub/file2.ext
    folder2/
    folder3
'''.strip()

_config_inst = None
# currently only supports nesting of 2
_config_overwrites = defaultdict(dict)

log = logging.getLogger(__name__)


def get_config_value(*args):
    # currently only supports nesting of 2
    if len(args) == 2:
        global _config_overwrites
        if args[1] in _config_overwrites[args[0]]:
            return _config_overwrites[args[0]][args[1]]

    global _config_inst
    if not _config_inst:
        return None

    try:
        value = _config_inst
        for arg in args:
            value = value[arg]
    except:
        return None

    return value


def get_config_value_as_list(*args):
    value = get_config_value(*args)
    return [] if value is None \
        else value.split(',') if value \
        else [] if value.empty \
        else [value]


def get_multiline_config_value_as_list(*args):
    value = get_config_value(*args)
    return [x.strip() for x in value.splitlines() if x] if value else value


# currently only supports nesting of 2
def set_config_value(category, key, value):
    global _config_overwrites
    _config_overwrites[category][key] = value


def load_or_create_configfile(config_path):
    global _config_inst
    _config_inst = configparser.ConfigParser()

    found_config = bool(_config_inst.read(config_path))
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
