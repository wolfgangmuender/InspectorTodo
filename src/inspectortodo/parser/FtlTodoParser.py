from .BaseTodoParser import BaseTodoParser


class FtlTodoParser(BaseTodoParser):
    def __init__(self, keywords):
        super().__init__('', '<#--', '-->', keywords)
