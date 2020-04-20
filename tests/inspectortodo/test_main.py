# Copyright 2018 TNG Technology Consulting GmbH, Unterfoehring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import io
from xml.etree import ElementTree

from inspectortodo.main import print_xml
from inspectortodo.todo import Todo

XML_CONTENT = '<?xml version="1.0" encoding="UTF-8"?>\n' \
              '<testsuite name="InspectorTodo" tests="4" failures="2">\n' \
              '\t<testcase classname="some/path" name="line 1" />\n' \
              '\t<testcase classname="some/path" name="line 2" />\n' \
              '\t<testcase classname="another/path" name="line 47" >\n' \
              '\t\t<failure message="this is an invalid todo">todoish</failure>\n' \
              '\t</testcase>\n' \
              '\t<testcase classname="another/path/again" name="line 47" >\n' \
              '\t\t<failure message="this is another invalid todo">Needs escaping: &lt;!--</failure>\n' \
              '\t</testcase>\n' \
              '</testsuite>\n'


def test_print_xml():
    valid_todo_1 = Todo('some/path', 1, 'todoish')
    valid_todo_2 = Todo('some/path', 2, 'todoish')
    invalid_todo_1 = Todo('another/path', 47, 'todoish')
    invalid_todo_1.mark_as_invalid('this is an invalid todo')
    invalid_todo_2 = Todo('another/path/again', 47, 'Needs escaping: <!--')
    invalid_todo_2.mark_as_invalid('this is another invalid todo')

    todos = [valid_todo_1, valid_todo_2, invalid_todo_1, invalid_todo_2]

    xml_file = io.StringIO()
    print_xml(xml_file, todos)
    xml_file.seek(0)
    xml_content = xml_file.read()

    assert XML_CONTENT == xml_content

    root = ElementTree.fromstring(xml_content)
    assert root is not None
