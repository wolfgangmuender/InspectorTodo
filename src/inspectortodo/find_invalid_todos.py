# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

from git import InvalidGitRepositoryError, Repo
import logging
import os
import sys

from .parser import (BashTodoParser, JavaTodoParser, PythonTodoParser, XmlTodoParser, PhpTodoParser, CsharpTodoParser,
                     JavaScriptTodoParser)
from .validator import (RegExpValidator, VersionsValidator)


log = logging.getLogger()

java_parser = JavaTodoParser(['TODO'])
bash_parser = BashTodoParser(['TODO'])
python_parser = PythonTodoParser(['TODO'])
xml_parser = XmlTodoParser(['TODO'])
php_parser = PhpTodoParser(['TODO'])
csharp_parser = CsharpTodoParser(['TODO'])
javascript_parser = JavaScriptTodoParser(['TODO'])


def find_invalid_todos(root_dir, ticket_pattern, version_pattern, version, versions):
    validators = [
        RegExpValidator(ticket_pattern)
    ]

    if versions is not None and version is not None:
        validators += VersionsValidator(versions, version)

    if version_pattern is not None:
        validators += RegExpValidator(version_pattern)

    log.info("Searching '%s' for forgotten todos.", root_dir)
    todos = traverse(root_dir)
    if not todos:
        log.info('No todos found.')
        return

    log.info('Validating %d todos.', len(todos))

    invalid_todos = []
    for todo in todos:
        for validator in validators:
            if validator.validate(todo):
                continue

        todo.mark_as_invalid('Todo is not conform to any validator!')
        invalid_todos.append(todo)

    if not invalid_todos:
        log.info('All todos are fine.')
        return

    log.error('------------------------------------------------------------------------------')
    log.error('Found {} invalid todos.'.format(len(invalid_todos)))
    log.error('------------------------------------------------------------------------------')
    for invalid_todo in invalid_todos:
        invalid_todo.print()
        log.error('------------------------------------------------------------------------------')


def traverse(root_dir):
    try:
        repository = Repo(root_dir)
        return traverse_git(repository)
    except InvalidGitRepositoryError:
        return traverse_folder(root_dir)


def traverse_git(repository):
    log.info("Traversing all files under git control in folder '{}'.".format(repository.working_dir))
    return traverse_tree(repository.tree())


def traverse_tree(tree):
    todos = []
    for sub_tree in tree.trees:
        todos += traverse_tree(sub_tree)
    for file in tree.blobs:
        todos += parse(file.abspath, file.path)
    return todos


def traverse_folder(root_dir):
    log.info("Traversing all files under folder '{}'.".format(root_dir))
    todos = []
    for (root_dir_name, dir_names, file_names) in os.walk(root_dir):
        for file_name in file_names:
            abs_file_name = os.path.join(os.path.abspath(root_dir_name), file_name)
            todos_for_file = parse(abs_file_name, get_relative_path(abs_file_name, root_dir))
            todos.extend(todos_for_file)
    return todos


def get_relative_path(path, root_dir):
    norm_path = os.path.normpath(path)
    path_split = norm_path.split(os.sep)
    norm_root_dir = os.path.normpath(root_dir)
    root_dir_split = norm_root_dir.split(os.sep)
    if len(path_split) <= len(root_dir_split):
        log.error('Error relativizing path for root_dir %s and path %s', norm_root_dir, norm_path)
        sys.exit(-1)
    return os.sep.join(path_split[len(root_dir_split):])


def parse(absolute_path, relative_path):
    log.debug("Parsing file {}".format(absolute_path))
    file_extension = os.path.splitext(absolute_path)[1]
    if file_extension == '.java':
        log.debug("Parsing Java file %s", relative_path)
        return java_parser.get_todos(absolute_path, relative_path)
    elif file_extension == '.py':
        log.debug("Parsing Python file %s", relative_path)
        return python_parser.get_todos(absolute_path, relative_path)
    elif file_extension == '.sh':
        log.debug("Parsing Shell file %s", relative_path)
        return bash_parser.get_todos(absolute_path, relative_path)
    elif file_extension == '.xml' or file_extension == '.xsd' or file_extension == '.wsdl':
        log.debug("Parsing xml file %s", relative_path)
        return xml_parser.get_todos(absolute_path, relative_path)
    elif file_extension == '.php':
        log.debug("Parsing PHP file %s", relative_path)
        return php_parser.get_todos(absolute_path, relative_path)
    elif file_extension == '.cs':
        log.debug("Parsing Csharp file %s", relative_path)
        return csharp_parser.get_todos(absolute_path, relative_path)
    elif file_extension == '.js':
        log.debug("Parsing JavaScript file %s", relative_path)
        return javascript_parser.get_todos(absolute_path, relative_path)
    else:
        log.debug("Skipping unknown file type of file %s", relative_path)
        return []
