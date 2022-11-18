from .BaseTodoParser import BaseTodoParser


class XmlTodoParser(BaseTodoParser):
    def __init__(self, keywords):
        super().__init__('', '<!--', '-->', keywords)
