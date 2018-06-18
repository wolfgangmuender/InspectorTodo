# Copyright 2018 TNG Technology Consulting GmbH, Unterfoehring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import io

from inspectortodo.main import print_xml
from inspectortodo.todo import Todo


XML_CONTENT = '<?xml version="1.0" encoding="UTF-8"?>\n' \
              '<testsuite name="InspectorTodo" tests="3" failures="1">\n' \
              '\t<testcase classname="some/path" name="line 1" />\n' \
              '\t<testcase classname="some/path" name="line 2" />\n' \
              '\t<testcase classname="another/path" name="line 47" >\n' \
              '\t\t<failure>this is an invalid todo</failure>\n' \
              '\t</testcase>\n' \
              '</testsuite>\n'


def test_print_xml():
    valid_todo_1 = Todo('some/path', 1, 'todoish')
    valid_todo_2 = Todo('some/path', 2, 'todoish')
    invalid_todo = Todo('another/path', 47, 'todoish')
    invalid_todo.mark_as_invalid('this is an invalid todo')

    todos = [valid_todo_1, valid_todo_2, invalid_todo]

    xml_file = io.StringIO()
    print_xml(xml_file, todos)
    xml_file.seek(0)
    xml_content = xml_file.read()

    assert XML_CONTENT == xml_content
