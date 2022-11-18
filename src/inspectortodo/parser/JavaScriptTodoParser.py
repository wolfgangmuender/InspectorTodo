from .BaseTodoParser import BaseTodoParser


class JavaScriptTodoParser(BaseTodoParser):
    def __init__(self, keywords):
        super().__init__('//', '/*', '*/', keywords)
