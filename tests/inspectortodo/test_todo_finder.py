# Copyright 2018 TNG Technology Consulting GmbH, Unterfoehring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import os

from inspectortodo.todo_finder import TodoFinder


def test_find_bare():
    # only searches in project_for_testing and subfolders
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'project_for_testing')
    todo_finder = TodoFinder(root_dir, [])
    todos = todo_finder.find()
    assert 5 == todo_finder.num_files
    assert 9 == len(todos)


def test_find_git():
    # searches in the _whole_ repository
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
    todo_finder = TodoFinder(root_dir, [])
    todos = todo_finder.find()
    assert 10 == todo_finder.num_files
    assert 9 == len(todos)
