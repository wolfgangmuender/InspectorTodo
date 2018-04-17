### About
InspectorTodo is a Python tool to track the status of todos in a software project, assuming that the project uses an issue tracker, e.g. JIRA. In its simplest form it searches for all occurences of the string TODO and checks whether it is followed by a ticket reference that is conform to a given regular expression.

Download or clone this project and go to the resulting directory (Python >= 3.6 is required):

    pip install .

Then you can run inspectortodo:

    inspectortodo --help

If you installed it in a virtualenv (which is recommended), then you always have to activate the virtualenv first.

### Copyright & License

InspectorTodo was conceived, written and executed by [Martin Fink](https://github.com/martin1fink),
[Kai Helbig](https://github.com/ostrya) and [Wolfgang M&uuml;nder](https://github.com/wolfgangmuender).

&copy; 2018 TNG Technology Consulting GmbH, Unterf&ouml;hring, Germany

Licensed under the Apache License, Version 2.0 - see [LICENSE.md](LICENSE.md) in project root directory.
