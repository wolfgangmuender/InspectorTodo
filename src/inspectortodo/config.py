# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import configparser
import logging
import sys
from typing import Optional


DEFAULT_CONFIG = '''
[jira_server]
url: https://example.local/jira
username: test
password: test

[statuses]
# mapping of issue types to allowed statuses
all: Backlog,Todo,In Progress

[files]
# whitelist of file paths where todos are not searched or validated, relative to the root directory
whitelist=
    folder/file1.ext
    sub/sub/file2.ext
'''.strip()

_config_inst: Optional[configparser.ConfigParser] = None

log = logging.getLogger(__name__)


def get_config_value(*args):
    global _config_inst
    if not _config_inst:
        return None

    value = _config_inst
    for arg in args:
        value = value[arg]

    return value


def get_config_value_as_list(*args):
    value = get_config_value(*args)
    return value.split(',') if value else value


def get_multiline_config_value_as_list(*args):
    value = get_config_value(*args)
    return [x.strip() for x in value.splitlines() if x] if value else value


def load_or_create_config(config_path):
    global _config_inst
    _config_inst = configparser.ConfigParser()

    found_config = bool(_config_inst.read(config_path))
    if found_config:
        log.info('Loaded config from "%s"', config_path)
    else:
        log.info('No config file at "%s"', config_path)
        create_default_config(config_path)
        sys.exit(0)


def create_default_config(config_path):
    try:
        with open(config_path, 'x', encoding='UTF-8') as config_file:
            config_file.write(DEFAULT_CONFIG)
    except FileExistsError:
        log.error('Config file "%s" already exists', config_path)
    else:
        log.info('Created config file at "%s"', config_path)
