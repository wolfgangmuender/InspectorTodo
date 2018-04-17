# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import logging


log = logging.getLogger()


class Todo:
    def __init__(self, file_path, line_number, content):
        self.file_path = file_path
        self.line_number = line_number
        self.content = content
        self.is_valid = True
        self.error_reason = None

    def __str__(self):
        return 'In file ' + self.file_path + ':' + str(self.line_number) + '\n' + self.content

    def mark_as_invalid(self, error_reason):
        self.is_valid = False
        self.error_reason = error_reason

    def print(self, show_valid=False):
        if not show_valid and self.is_valid:
            return

        log.error('[REASON]   %s' % self.error_reason)
        log.error('[FILE]     %s' % self.file_path)
        log.error('[LINE]     %s' % self.line_number)
        log.error('[CONTENT]  %s' % self.content)
