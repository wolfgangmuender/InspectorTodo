from .BaseTodoParser import BaseTodoParser


class BashTodoParser(BaseTodoParser):
    def __init__(self, keywords):
        super().__init__('#', '', '', keywords)
