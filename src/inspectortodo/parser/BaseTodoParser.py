# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import functools
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
        self.annotations = annotations
        self.multi_line_comment_start = multi_line_comment_start
        self.multi_line_comment_end = multi_line_comment_end
        self.keywords = keywords
        self.comment_content = ''
        self.context = Context.code
        self.todos = []
        self.line_number = 1

    def get_todos(self, absolute_file_name, relative_file_path):
        try:
            with(open(absolute_file_name, encoding='utf-8')) as file:
                self.comment_content = ''
                self.context = Context.code
                self.todos = []
                self.line_number = 1
                f_read_ch = functools.partial(file.read, 1)
                for ch in iter(f_read_ch, ''):
                    if self.context == Context.code:
                        if self.matches_single_line_comment_start(ch, file):
                            self.context = Context.single_line_comment
                            self.comment_content = self.single_line_comment_start
                        elif self.matches_multi_line_comment_start(ch, file):
                            self.context = Context.multi_line_comment
                            self.comment_content = self.multi_line_comment_start
                        else:
                            annotation = self.find_matching_annotations(ch, file)
                            if annotation is not None:
                                self.context = Context.annotation
                                self.comment_content = annotation
                    elif self.context == Context.single_line_comment and ch == LINE_BREAK:
                        self.store_if_todo_and_reset(relative_file_path)
                    elif self.context == Context.annotation and ch == LINE_BREAK:
                        self.store_if_todo_and_reset(relative_file_path, True)
                    elif self.context == Context.multi_line_comment and self.matches_multi_line_comment_end(ch, file):
                        self.comment_content += self.multi_line_comment_end
                        self.store_if_todo_and_reset(relative_file_path)
                    else:
                        self.comment_content += ch
                    if ch == LINE_BREAK:
                        self.line_number += 1
            return self.todos
        except Exception as e:
            log.warning('Error parsing file {}: {}', relative_file_path, e)
            return []

    def matches_single_line_comment_start(self, character, file):
        return self.matches(character, self.single_line_comment_start, file)

    def find_matching_annotations(self, character, file):
        if self.annotations is None:
            return None
        for annotation in self.annotations:
            if self.matches(character, annotation, file):
                return annotation
        return None

    def matches_multi_line_comment_start(self, character, file):
        return self.matches(character, self.multi_line_comment_start, file)

    def matches_multi_line_comment_end(self, character, file):
        return self.matches(character, self.multi_line_comment_end, file)

    def matches(self, character, string_to_match, file):
        if len(string_to_match) > 0 and character == string_to_match[0]:
            potential_match = character + file.read(len(string_to_match)-1)
            return potential_match == string_to_match
        return False

    def store_if_todo_and_reset(self, file_path, is_annotation=False):
        if is_annotation or self.comment_contains_todo(self.comment_content):
            self.todos.append(Todo(file_path, self.line_number, self.comment_content))
        self.comment_content = ''
        self.context = Context.code

    def comment_contains_todo(self, content):
        for keyword in self.keywords:
            if keyword in content:
                return True
        return False
