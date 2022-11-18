import os

from inspectortodo.parser import XmlTodoParser
from inspectortodo.todo_finder import TODO_KEYWORDS


def test_xml_parsing():
    xml_file_relative = os.path.join('xml', 'test.xml')
    xml_file_absolute = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'project_for_testing',
                                     xml_file_relative)

    xml_parser = XmlTodoParser(TODO_KEYWORDS)
    todos = xml_parser.get_todos(xml_file_absolute, xml_file_relative)

    assert 1 == len(todos)
    assert '<!-- TODO IT-1234 Do something -->' == todos[0].content
