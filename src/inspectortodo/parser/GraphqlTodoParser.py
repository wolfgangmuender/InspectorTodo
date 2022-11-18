from .BaseTodoParser import BaseTodoParser


class GraphqlTodoParser(BaseTodoParser):
    def __init__(self, keywords):
        super().__init__('#', '"""', '"""', keywords)
