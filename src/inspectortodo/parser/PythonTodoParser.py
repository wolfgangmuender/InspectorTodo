from .BaseTodoParser import BaseTodoParser


class PythonTodoParser(BaseTodoParser):
    def __init__(self, keywords):
        super().__init__('#', '"""', '"""', keywords)
