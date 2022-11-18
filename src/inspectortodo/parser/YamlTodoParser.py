from .BaseTodoParser import BaseTodoParser


class YamlTodoParser(BaseTodoParser):
    def __init__(self, keywords):
        super().__init__('#', '', '', keywords)
