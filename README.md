# I/O Tools

___
Data/file manipulation tools to prevent me from having to write out json serilization a million times. Tries to make you code your variables in a a way that can lift-and-shift easily.

## Usage

___

```python
import io_tools as io # custom lib

debug = True
go_steppy = False
working_directory = os.getcwd()

#load the settings file
settings_file = sys.argv[1]
settings = io.read_file(settings_file)
vars = Vars(settings, debug, go_steppy)

#set some env vars
vars.change_value('working_dir', working_directory, debug)

```

__To Use:__

```bash
# cd to the program folder
cd data_transformation

# install dependancies
pip3 install -r requirements.txt

# run the script
python3 yaml_to_json_convert.py

```

__Examples:__

```python

import data_transformation as io
import json

debug = True
go_steppy = False
input_file = "pref_input_test.yaml"

# reads a yaml file
settings = io.read_file(input_file, debug)

# print as pretty json
io.print_pretty(settings, debug, "json")

#print as compact json
print(settings)

# print as yaml
io.print_pretty(settings, debug, "yaml")

# stringify
vars = io.Variables(settings, debug, go_steppy)

# print
io.print_pretty(settings, debug, "yaml")
io.print_pretty(settings, debug, "json")
print(vars.work[0]['name'])

# convert to csv
io.write_file("test.json", vars.__dict__, debug, "json")
io.json_to_csv("test.json", debug)
```

## Class Methods

___
### Datastore

 Datastore is a `<key>:<value>` dict that accepts any  types and is used for portability. It achieves this  by storing all variables in a generic dictionary  with the `change()` method overriden to be an event system.

### Variables

 Object that holds a list of `Datastore()`s,
 When eneabled, the built-in `go_steppy()` function  will pause script execution on any memory state  change to provide a json formatted diff. for example:

 ![go_steppy](go_steppy.png)

  change_value:
    Triggered when any variable within the `Datastore()`  is updated, or created.
  get_current_value:
    Returns the current value of a variable within the `Datastore()`, and triggers an event.
  diff_values:
    When enabled, deepdiffs the current and proposed change to the `Datastore()` object
