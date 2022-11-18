from inspectortodo.todo import Todo
from inspectortodo.validator import RegExpValidator


def test_validation_via_regular_expression():
    pattern = r'SP-\d+'
    valid_todo = Todo('some path', 23, 'content containing valid issue reference SP-4711')
    invalid_todo = Todo('some path', 23, 'content containing invalid issue reference PS-4711')

    validator = RegExpValidator(pattern)
    assert validator.validate(valid_todo)
    assert not validator.validate(invalid_todo)
