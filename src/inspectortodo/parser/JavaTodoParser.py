from .BaseTodoParser import BaseTodoParser


JAVA_ANNOTATIONS = ['@Disabled', '@Ignore']


class JavaTodoParser(BaseTodoParser):
    def __init__(self, keywords):
        super().__init__('//', '/*', '*/', keywords, JAVA_ANNOTATIONS)
