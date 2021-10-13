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
```
#/usr/bin/env Python3
"""
Demo script to showcase the io_tools library and what it can do for you
"""

import io_tools as io
import sys
from pygments.styles import get_all_styles

# we make the assumption taht just about anything you will be doing has the option to
# export and import either json or yaml. Therefore, io_tools simply injests and holds
# your data as a JSON object. This makes it highly portable.

# Here is our memory represented as json
settings = {}

# lets initialize the object
vars = io.Variables(settings)

# Now assign some values
vars.go_steppy = True
vars.text_format = "yaml"
vars.debug = True

# Pretty print the cache
io.print_pretty(f"{vars.go_steppy}", vars.debug, vars.text_format)

# instect the cache size
print(f"{sys.getsizeof(vars)} bytes")

print(vars)
print(vars.__dict__)

# save the cache to a file
io.write_file('cache.json', print(vars.__dict__), vars.debug)

# delete
del vars
```

