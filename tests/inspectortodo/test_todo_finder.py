# Copyright 2018 TNG Technology Consulting GmbH, Unterfoehring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import os

from inspectortodo.todo_finder import TodoFinder


def test_find():
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'project_for_testing')
    todo_finder = TodoFinder(root_dir, [])
    todos = todo_finder.find()
    assert 5 == len(todos)
    assert 2 == todo_finder.num_files
