# Copyright 2018 TNG Technology Consulting GmbH, Unterfoehring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import os

from git import Repo

from inspectortodo.todo_finder import TodoFinder

FIND_GIT_NUM_FILES = 15
FIND_BARE_NUM_FILES = 9
NUM_TODOS = 14


def test_find_bare():
    # only searches in project_for_testing and subfolders
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'project_for_testing')
    todo_finder = TodoFinder(root_dir, [])
    todos = todo_finder.find()
    assert todo_finder.num_files == FIND_BARE_NUM_FILES
    assert len(todos) == NUM_TODOS


def test_find_git():
    # searches in the _whole_ repository
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
    todo_finder = TodoFinder(root_dir, [])
    todos = todo_finder.find()
    assert todo_finder.num_files == FIND_GIT_NUM_FILES
    assert len(todos) == NUM_TODOS


def test_git_grep_does_not_raise_exception_when_nothing_is_found():
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
    repository = Repo(root_dir)
    file_names = TodoFinder._git_grep(repository, "this must not" + "be found")
    assert len(file_names) == 0


def test_whitelist_file():
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
    todo_finder = TodoFinder(root_dir, ['tests/inspectortodo/project_for_testing/java/Versions.java'])
    todos = todo_finder.find()
    assert todo_finder.num_files == FIND_GIT_NUM_FILES - 1
    assert len(todos) == NUM_TODOS - 3


def test_whitelist_folder():
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
    todo_finder = TodoFinder(root_dir, ['tests/inspectortodo/project_for_testing/java/'])
    todos = todo_finder.find()
    assert todo_finder.num_files == FIND_GIT_NUM_FILES - 3
    assert len(todos) == NUM_TODOS - 6


def test_whitelist_file_and_folder():
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
    todo_finder = TodoFinder(root_dir, ['tests/inspectortodo/project_for_testing/java/Versions.java',
                                        'tests/inspectortodo/project_for_testing/java_script/'])
    todos = todo_finder.find()
    assert todo_finder.num_files == FIND_GIT_NUM_FILES - 2
    assert len(todos) == NUM_TODOS - 5
