# Copyright 2018 TNG Technology Consulting GmbH, Unterfoehring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import os

from git import Repo

from inspectortodo.todo_finder import TodoFinder


def test_find_bare():
    # only searches in project_for_testing and subfolders
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'project_for_testing')
    todo_finder = TodoFinder(root_dir, [])
    todos = todo_finder.find()
    assert 6 == todo_finder.num_files
    assert 11 == len(todos)


def test_find_git():
    # searches in the _whole_ repository
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
    todo_finder = TodoFinder(root_dir, [])
    todos = todo_finder.find()
    assert 11 == todo_finder.num_files
    assert 11 == len(todos)


def test_git_grep_does_not_raise_exception_when_nothing_is_found():
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
    repository = Repo(root_dir)
    file_names = TodoFinder._git_grep(repository, "this must not" + "be found")
    assert 0 == len(file_names)
