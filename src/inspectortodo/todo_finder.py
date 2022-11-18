import logging
import os

from git import GitError, InvalidGitRepositoryError, Repo

from .parser import (BashTodoParser, JavaTodoParser, PythonTodoParser, XmlTodoParser, PhpTodoParser, CsharpTodoParser,
                     JavaScriptTodoParser, YamlTodoParser, FtlTodoParser, GraphqlTodoParser, JAVA_ANNOTATIONS)

TODO_KEYWORDS = ['TODO']

log = logging.getLogger()


class TodoFinder(object):

    def __init__(self, root_dir, paths_ignore_list):
        self.root_dir = root_dir
        self.paths_ignore_list = paths_ignore_list
        self.todo_keywords = TODO_KEYWORDS

        self.java_parser = JavaTodoParser(self.todo_keywords)
        self.bash_parser = BashTodoParser(self.todo_keywords)
        self.python_parser = PythonTodoParser(self.todo_keywords)
        self.xml_parser = XmlTodoParser(self.todo_keywords)
        self.php_parser = PhpTodoParser(self.todo_keywords)
        self.csharp_parser = CsharpTodoParser(self.todo_keywords)
        self.javascript_parser = JavaScriptTodoParser(self.todo_keywords)
        self.yaml_parser = YamlTodoParser(self.todo_keywords)
        self.ftl_parser = FtlTodoParser(self.todo_keywords)
        self.graphql_parser = GraphqlTodoParser(self.todo_keywords)

        self.num_files = 0

    def find(self):
        log.info("Searching '%s' for todos.", self.root_dir)
        try:
            repository = Repo(self.root_dir)
            todos = self._search_git(repository)
        except InvalidGitRepositoryError:
            todos = self._traverse_folder()

        log.info('Found %d todos in %d files.', len(todos), self.num_files)

        return todos

    def _search_git(self, repository):
        log.info("Grepping all files under git control in folder '%s'.", repository.working_dir)
        keywords = self.todo_keywords + JAVA_ANNOTATIONS

        file_names = []
        for keyword in keywords:
            file_names = file_names + self._git_grep(repository, keyword)
        file_names = list(set(file_names))

        todos = []
        for file_name in file_names:
            todos += self._parse(os.path.join(os.path.abspath(self.root_dir), file_name), file_name)

        return todos

    @staticmethod
    def _git_grep(repository, keyword):
        status, files_string, err = repository.git.grep('-l', keyword, with_extended_output=True, with_exceptions=False)
        if status == 1:
            log.debug("No result found.")
        elif status > 1:
            raise GitError("Command git grep returned status {} with error {}".format(status, err))
        return [x.strip() for x in files_string.splitlines() if x] if files_string else []

    def _traverse_folder(self):
        log.info("Traversing all files under folder '%s'.", self.root_dir)
        todos = []
        for (root_dir_name, dir_names, file_names) in os.walk(self.root_dir):
            for file_name in file_names:
                abs_file_name = os.path.join(os.path.abspath(root_dir_name), file_name)
                todos_for_file = self._parse(abs_file_name, os.path.relpath(abs_file_name, self.root_dir))
                todos.extend(todos_for_file)
        return todos

    def _parse(self, absolute_path, relative_path):
        if any(relative_path.startswith(ignored_path) for ignored_path in self.paths_ignore_list):
            log.debug("Skipping file %s", relative_path)
            return []

        if self.num_files > 0 and self.num_files % 1000 == 0:
            log.info("Total files parsed: %d", self.num_files)

        log.debug("Parsing file %s", absolute_path)
        self.num_files += 1

        file_extension = os.path.splitext(absolute_path)[1]
        if file_extension == '.java':
            log.debug("Parsing Java file %s", relative_path)
            return self.java_parser.get_todos(absolute_path, relative_path)
        elif file_extension == '.py':
            log.debug("Parsing Python file %s", relative_path)
            return self.python_parser.get_todos(absolute_path, relative_path)
        elif file_extension == '.sh':
            log.debug("Parsing Shell file %s", relative_path)
            return self.bash_parser.get_todos(absolute_path, relative_path)
        elif file_extension == '.xml' or file_extension == '.xsd' or file_extension == '.wsdl':
            log.debug("Parsing xml file %s", relative_path)
            return self.xml_parser.get_todos(absolute_path, relative_path)
        elif file_extension == '.php':
            log.debug("Parsing PHP file %s", relative_path)
            return self.php_parser.get_todos(absolute_path, relative_path)
        elif file_extension == '.cs':
            log.debug("Parsing Csharp file %s", relative_path)
            return self.csharp_parser.get_todos(absolute_path, relative_path)
        elif file_extension == '.js':
            log.debug("Parsing JavaScript file %s", relative_path)
            return self.javascript_parser.get_todos(absolute_path, relative_path)
        elif file_extension == '.vue':
            log.debug("Parsing Vue.js single-file component file %s", relative_path)
            js_todos = self.javascript_parser.get_todos(absolute_path, relative_path)
            xml_todos = self.xml_parser.get_todos(absolute_path, relative_path)
            return js_todos + xml_todos
        elif file_extension == '.yml' or file_extension == '.yaml':
            log.debug("Parsing Yaml file %s", relative_path)
            return self.yaml_parser.get_todos(absolute_path, relative_path)
        elif file_extension == '.ftl':
            log.debug("Parsing Ftl file %s", relative_path)
            return self.ftl_parser.get_todos(absolute_path, relative_path)
        elif file_extension == '.ts':
            log.debug("Parsing TypeScript file %s", relative_path)
            js_todos = self.javascript_parser.get_todos(absolute_path, relative_path)
            graphql_todos = self.graphql_parser.get_todos(absolute_path, relative_path)
            return js_todos + graphql_todos
        elif file_extension == '.graphql':
            log.debug("Parsing Graphql file %s", relative_path)
            return self.graphql_parser.get_todos(absolute_path, relative_path)
        else:
            log.debug("Skipping unknown file type of file %s", relative_path)
            return []
