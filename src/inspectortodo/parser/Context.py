from enum import Enum


class Context(Enum):
    code = 0
    single_line_comment = 1
    multi_line_comment = 2
    annotation = 3
