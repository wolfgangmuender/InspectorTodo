import logging

from .Context import Context
from inspectortodo.todo import Todo

LINE_BREAK = '\n'
log = logging.getLogger()


class BaseTodoParser(object):
    """ Finds todos in file """

    def __init__(self, single_line_comment_start, multi_line_comment_start, multi_line_comment_end, keywords,
                 annotations=None):
        self.single_line_comment_start = single_line_comment_start
        self.multi_line_comment_start = multi_line_comment_start
        self.multi_line_comment_end = multi_line_comment_end
        self.keywords = keywords
        self.annotations = annotations

    def get_todos(self, absolute_file_name, relative_file_path):
        self._init_variables()

        try:
            with(open(absolute_file_name, mode='r', encoding='utf-8')) as file:
                file_iterator = FileIterator(file)
                for ch in file_iterator:
                    if self.context == Context.code:
                        if self.matches_single_line_comment_start(ch, file_iterator):
                            self.context = Context.single_line_comment
                            self.comment_content = ch
                        elif self.matches_multi_line_comment_start(ch, file_iterator):
                            self.context = Context.multi_line_comment
                            self.comment_content = ch
                        else:
                            annotation = self.find_matching_annotations(ch, file_iterator)
                            if annotation is not None:
                                self.context = Context.annotation
                                self.comment_content = ch
                    elif self.context == Context.single_line_comment and ch == LINE_BREAK:
                        self._store_if_todo_and_reset(file_iterator, relative_file_path)
                    elif self.context == Context.annotation and ch == LINE_BREAK:
                        self._store_if_todo_and_reset(file_iterator, relative_file_path, True)
                    elif self.context == Context.multi_line_comment \
                            and self.matches_multi_line_comment_end(ch, file_iterator):
                        self.comment_content += self.multi_line_comment_end
                        self._store_if_todo_and_reset(file_iterator, relative_file_path)
                    else:
                        self.comment_content += ch
            return self.todos
        except Exception as e:
            log.warning('Error parsing file %s: %s', relative_file_path, e)
            return []

    def _init_variables(self):
        self.comment_content = ''
        self.context = Context.code
        self.todos = []

    def matches_single_line_comment_start(self, character, file_iterator):
        return self._matches(character, self.single_line_comment_start, file_iterator)

    def matches_multi_line_comment_start(self, character, file_iterator):
        return self._matches(character, self.multi_line_comment_start, file_iterator)

    def matches_multi_line_comment_end(self, character, file_iterator):
        return self._matches(character, self.multi_line_comment_end, file_iterator)

    def find_matching_annotations(self, character, file_iterator):
        if self.annotations:
            for annotation in self.annotations:
                if self._matches(character, annotation, file_iterator):
                    return annotation
        return None

    def _matches(self, character, string_to_match, file_iterator):
        if len(string_to_match) > 0 and character == string_to_match[0]:
            potential_match = character + file_iterator.look_ahead(len(string_to_match) - 1)
            return potential_match == string_to_match
        return False

    def _store_if_todo_and_reset(self, file_iterator, file_path, is_annotation=False):
        if is_annotation or self._comment_contains_todo(self.comment_content):
            self.todos.append(Todo(file_path, file_iterator.line_number, self.comment_content))
        self.comment_content = ''
        self.context = Context.code

    def _comment_contains_todo(self, content):
        for keyword in self.keywords:
            if keyword in content:
                return True
        return False


class FileIterator:

    def __init__(self, file):
        self.file = file
        self.line_number = 1
        self._buffer = []

    def __iter__(self):
        return self

    def __next__(self):
        ch = self._get_next_char()
        if ch == LINE_BREAK:
            self.line_number += 1
        if ch:
            return ch
        else:
            raise StopIteration()

    def _get_next_char(self):
        if len(self._buffer) > 0:
            return self._buffer.pop(0)
        return self.file.read(1)

    def look_ahead(self, n):
        buffer_len = len(self._buffer)
        for _ in range(buffer_len, n):
            self._buffer.append(self.file.read(1))

        return ''.join(self._buffer[:n])
