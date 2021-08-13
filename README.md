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

## Functions

___

### >get_timestamp

 Returns a timestamp in `DD:MMM:YYYY (HH:MM:SS.f)` format

### >read_file

 Reads json file from path: returns json object

### >azure_auto_instal

 Attempts to force azure cli to auto-install cost management module

### >print_pretty

 Prettified json console output: returns `<string>`

### >colorize_json

 Prints colorful json

### >vailidate_json_file

 Takes a `file_path`, returns `query{dict(<string>,<string>)}`

### >validate_json_object

 Takes a `file_path`, returns `query{dict(<string>,<string>)}`

### >write_file

 Attempt to save <payload> to disk at <path> as json file

### >update_file

 Update an existing file on disk

### >make_dir

 Makes/deletes directory


## Class Methods

___
### >Datastore()

 Datastore is a `<key>:<value>` dict that accepts any  types and is used for portability. It achieves this  by storing all variables in a generic dictionary  with the `change()` method overriden to be an event  system.

### Variables()

 Object that holds a list of `Datastore()`s,
 When eneabled, the built-in `go_steppy()` function  will pause script execution on any memory state  change to provide a json formatted diff. for example:

 ![go_steppy](go_steppy.png)

### change_value()

 Triggered when any variable within the `Datastore()`  is updated, or created.

### get_current_value()

 Returns the current value of a variable within the `Datastore()`, and triggers an event.

### diff_values()

 When enabled, deepdiffs the current and proposed change to the `Datastore()` object
