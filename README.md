### About

InspectorTodo is a Python tool to track the status of todos in a software project, assuming that the project uses an 
issue tracker, e.g. JIRA. In its simplest form it searches for all occurences of the string TODO and checks whether it 
is followed by an issue reference that is conform to a given regular expression.

Download or clone this project and go to the resulting directory (Python >= 3.6 is required):

    pip install .

Then you can run InspectorTodo:

    inspectortodo --help

If you installed it in a virtualenv (which is recommended), then you always have to activate the virtualenv first.

### Example

The source code of InspectorTodo contains a small example project which can be parsed with the command (assuming you
are at project root)

    inspectortodo ./tests/inspectortodo/test_project "IT-\d+" --version-pattern "Release-\d+" --version 2 --versions 1,2,3

### Config file

To use advanced features you can use a config file by passing a file path via the --configfile option. If the file does 
not exist a default config is created which you can adapt afterwards.

### Copyright & License

InspectorTodo was conceived, written and executed by [Martin Fink](https://github.com/martin1fink),
[Kai Helbig](https://github.com/ostrya) and [Wolfgang M&uuml;nder](https://github.com/wolfgangmuender).

&copy; 2018 TNG Technology Consulting GmbH, Unterf&ouml;hring, Germany

Licensed under the Apache License, Version 2.0 - see [LICENSE.md](LICENSE.md) in project root directory.
