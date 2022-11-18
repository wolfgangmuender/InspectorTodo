from io import StringIO

from inspectortodo.parser.BaseTodoParser import FileIterator


def test_iterate_file():
    file_iterator = _get_file_iterator_with_content('abc')

    chars = []
    for ch in file_iterator:
        chars.append(ch)
    assert 3 == len(chars)
    assert 'a' == chars[0]
    assert 'b' == chars[1]
    assert 'c' == chars[2]


def test_line_number():
    file_iterator = _get_file_iterator_with_content('ab\nd\nef')
    for ch in file_iterator:
        if ch == 'a' or ch == 'b':
            assert 1 == file_iterator.line_number
        elif ch == 'd':
            assert 2 == file_iterator.line_number
        elif ch == 'e' or ch == 'f':
            assert 3 == file_iterator.line_number


def test_look_ahead_does_not_change_next():
    file_iterator = _get_file_iterator_with_content('abc')
    chars = []
    for ch in file_iterator:
        if ch == 'a':
            assert 'b' == file_iterator.look_ahead(1)
            assert 'bc' == file_iterator.look_ahead(2)
        elif ch == 'b':
            assert 'c' == file_iterator.look_ahead(1)
            assert 'c' == file_iterator.look_ahead(2)
        chars.append(ch)
    assert 3 == len(chars)
    assert 'a' == chars[0]
    assert 'b' == chars[1]
    assert 'c' == chars[2]


def _get_file_iterator_with_content(content):
    test_stream = StringIO()
    test_stream.write(content)
    test_stream.seek(0)

    return FileIterator(test_stream)
