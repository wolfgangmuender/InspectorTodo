# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

from git import InvalidGitRepositoryError, Repo
import logging
import os

from .parser import (BashTodoParser, JavaTodoParser, PythonTodoParser, XmlTodoParser, PhpTodoParser, CsharpTodoParser,
                     JavaScriptTodoParser)


log = logging.getLogger()


class TodoFinder(object):

    def __init__(self, root_dir, files_whitelist):
        self.root_dir = root_dir
        self.files_whitelist = files_whitelist

        self.java_parser = JavaTodoParser(['TODO'])
        self.bash_parser = BashTodoParser(['TODO'])
        self.python_parser = PythonTodoParser(['TODO'])
        self.xml_parser = XmlTodoParser(['TODO'])
        self.php_parser = PhpTodoParser(['TODO'])
        self.csharp_parser = CsharpTodoParser(['TODO'])
        self.javascript_parser = JavaScriptTodoParser(['TODO'])

        self.num_files = 0

    def find(self):
        log.info("Searching '%s' for todos.", self.root_dir)
        try:
            repository = Repo(self.root_dir)
            todos = self._traverse_git(repository)
        except InvalidGitRepositoryError:
            todos = self._traverse_folder()

        log.info('Found %d todos in %d files.', len(todos), self.num_files)

        return todos

    def _traverse_git(self, repository):
        log.info("Traversing all files under git control in folder '%s'.", repository.working_dir)
        return self._traverse_tree(repository.tree())

    def _traverse_tree(self, tree):
        todos = []
        for sub_tree in tree.trees:
            todos += self._traverse_tree(sub_tree)
        for file in tree.blobs:
            todos += self._parse(file.abspath, file.path)
        return todos

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
        if relative_path in self.files_whitelist:
            log.debug("Skipping whitelisted file %s", relative_path)
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
        else:
            log.debug("Skipping unknown file type of file %s", relative_path)
            return []
