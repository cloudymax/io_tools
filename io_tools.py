#/usr/bin/python3
# TODO: cleanup base libs
import json
from datetime import datetime
import logging
import sys
from deepdiff import DeepDiff
from dictor import dictor
# TODO: use me
import logging as log
from logging import debug
import os
import pandas as pd
import pathlib
from pyfiglet import Figlet
from pygments import highlight
from pygments.lexers.data import JsonLexer
from pygments.lexers.data import YamlLexer
from pygments.lexers import get_lexer_by_name
from pygments.formatters import (Terminal256Formatter,
                                 HtmlFormatter,
                                 TerminalFormatter)
import simplejson
import re
import shutil
import time
import yaml
from yaml.loader import SafeLoader


# TODO: Logging
log_level = log.DEBUG
program_log = log.getLogger(f"io_tools")
log.basicConfig(level=log_level)
program_log.info("logging config loaded")



def get_timestamp():
    """
    returns a timestamp in DD:MMM:YYYY (HH:MM:SS.f) format
    """

    now = datetime.now()
    timestamp = now.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    return timestamp


def get_epoch():
    """
    returns a timestamp in epoch format
    """

    # logging
    ts = get_timestamp()
    #program_log.debug(f"function 'get_epoch' called at {ts}")

    timestamp = time.time()

    return timestamp


def read_file(path: str):
    """
    reads json file from <path>: returns <json object>
    """

    # logging
    ts = get_timestamp()
    #program_log.debug(f"function 'read_file' called at {ts}")

    # try to read the file
    #program_log.debug(f"trying to read: {path}")

    file_extension = pathlib.Path(path).suffix

    if file_extension == ".yaml":
        try:
            data = read_yaml_file(path)
            #program_log.debug(f"successfully read: {path}")

        except Exception:
            #program_log.error(f"Failed to read: {path}")
            data = False

    if file_extension == ".json":
        try:
            data = read_json_file(path)
            #program_log.debug(f"successfully read: {path}")

        except Exception:
            program_log.error(f"Failed to read: {path}")
            data = False

    confirmed_data = validate_json_object(data)
    return confirmed_data['path']


def read_yaml_file(yaml_file_path):
    """
    Reads a .yaml file as raw, converts to json, formats it, then
    reloads it as a dict for uniformity of transformation later
    """

    with open(yaml_file_path, 'r') as f:

        # reads the files as raw - unusable until loaded
        raw = f.read()
        #print(raw)

        # converts the raw data into a json string
        yaml_object = yaml.safe_load(raw)
        #print(yaml_object)

        # pretty format the json to make it uniform
        json_data = json.dumps(yaml_object, separators=(',', ":"))
        #print(json_data)

        # Load the clean json into a python dict
        json_object = json.loads(f"{json_data}")
        #print(json_object)

    return json_object


def read_json_file(json_file_path):
    """
    This function reads a .json file as raw and converts to a json dict via json.loads()
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:

        # read the file as raw data
        raw = f.read()

        # convert the raw string into a json object
        json_object = json.loads(raw)

    return json_object


def json_to_yaml(json_data):
    """
    converts json_data: str into a json object{}
    converts the json object{} into a yaml: str
    """
    data = yaml.dump(simplejson.loads(str(json_data)), default_flow_style=False)
    return data


def yaml_to_json(yaml_file):
    """
    converts a yaml string into an object
    dumps the object as json
    """
    with open(yaml_file, 'r') as f:
      raw = f.read()
      yaml_object = yaml.safe_load(raw)
      json_data = json.dumps(yaml_object, separators=(',', ":"))

    return json_data


def json_to_csv(json_file_path):
    """
    dump a json object to a file, then convert the file to a csv
    """
    with open(json_file_path, encoding='utf-8-sig') as f_input:
        df = pd.read_json(f_input)
        df.to_csv('test.csv', encoding='utf-8', index=False)


def colorize_json(json_data, debug):
    """
    print colorful json data
    """

    # dump json to a string
    data = json.dumps(json.loads(json_data),
                        indent="  ",
                        separators=(',',': '),
                        sort_keys=True,
                        skipkeys=False)


    # create the highlighted text
    colorful = highlight(
        data,
        lexer=get_lexer_by_name("json"),
        formatter=Terminal256Formatter(style="fruity", linenos=True),
    )

    # print the highlighted text
    if debug == True:
        print(colorful)
    else:
        log = {}
        log['time'] = get_timestamp()
        log['data'] = colorful
        (log, True)


def colorize_yaml(data, debug):
    """
    prints colorful yaml data
    """

    # create highlighted text
    colorful = highlight(
        data,
        lexer=get_lexer_by_name("yaml"),
        formatter=Terminal256Formatter(style="fruity", linenos=True),
    )

    # print the highlighted text
    if debug == True:
        print(colorful)
    else:
        program_log.debug(colorful)


def validate_json_file(path: str, debug=False, format="json"):
    """
    takes a <file_path>, returns query{dict(<string>,<string>)}
    """
    #program_log.debug(f"json validation requested for : {path} ")

    query = {}
    query['path'] = path
    if read_file(path, debug) == False:
        query['readable'] = False
    else:
        query['readable'] = True
        program_log.error(f"Validation success : {path} was readable json")

    return query


def validate_json_object(object):
    """
    takes a jsonObject, returns query{dict(<string>,<string>)}
    """
    query = {}
    try:
        # is it already json?
        is_json = json.loads(object)
        query['readable'] = True
        query['path'] = object

    except Exception as e:
        # nope not already json
        program_log.error(f"Oof", print(e.__class__), "occurred")

        try:
        # can I make it json?
            raw_json = json.dumps(object,
                                  separators=(',', ': '),
                                  sort_keys=True,
                                  skipkeys=True)

            program_log.debug(f"Validation success : {object} was readable json")
            query['readable'] = True
            query['path'] = raw_json

        except Exception as e:
        # nope, cant make it json :(
            program_log.error(f"Oof", print(e.__class__), "occurred")
            program_log.error(f"Validation failure : {object} was not readable json")

            query['readable'] = False
            if debug:
                name = input("Any key to continue")

    return query

def print_pretty(data, debug=False, format: str = "json"):
    """
    prettified json console output: returns <string>
    Generate JSON
    """
    json_data = {}

    # Verify all the data we pass aound is valid json format
    try:
        json_data = validate_json_object(data)

    except Exception as e:
        program_log.error(f"Oof", print(e.__class__), "occurred")

    # once we determine it is readable, pretty print the data
    if json_data['readable'] != False:
        try:
            if format == "yaml":
            #if YAML formatted
                yaml_string = json_to_yaml(data)
                colorize_yaml(yaml_string, debug)
            else:
            #if JSON formatted
                if format == "json":
                    colorize_json(json_data['path'], debug)

        except Exception:
            print(f"Unable to parse data: {json_data}")
            if debug:
                name = input("Any key to continue")

def write_file(path: str, payload: str, debug = False, format="json"):
    """
    attempt to save <payload> to disk at <path> as json file
    """
    # check if the file and path exist on the target system,
    # if not, create it. return an error if we fail
    if not os.path.isfile(path):
        try:
            program_log.log(f"trying to write file: {path}", debug, format)
            text = dictor(payload, pretty=True)
            with open(path, "w") as save_file:
                save_file.write(text)
        except Exception as e:
            program_log.error(f"Oof", print(e.__class__), "occurred")
            program_log.error(f"failed to save: {path}", debug, format)
            if debug:
               name = input("Any key to continue")
    else:
    # if the file DOES exist, pop up a warning that I'm about to delete it.
        try:

            program_log.error(f"# file already exists: {path}", debug, format)

            desc = ("# if you dont want to delete the contents of the " +
                    "file on write, use the update_file() function")
            program_log.error(f"{desc}")

            program_log.error(f"# clearing file... {path}")

            # actually delete the file
            os.remove(path)

            # now try the whole loop again
            write_file(path, payload, debug)
        except Exception as e:
            program_log.error(f"Oof", print(e.__class__), "occurred")
            program_log.error(f"failed to save: {path}")
            if debug:
                name = input("Any key to continue")

    # validate that we can read the file we wrote
    validate_json_file(path, debug)


def update_file(path: str, payload: str, debug = False, format="json"):
    """
    update an existing file on disk
    """
    try:
        with open(path, "a") as save_file:
            save_file.write(payload)
            save_file.close()
    except Exception as e:
        program_log.error(f"Oof", print(e.__class__), "occurred")
        program_log.error(f"failed to update: {path}")


def make_dir(path: str, clear: bool = False, debug: bool = False,
             format="json"):
    """
    makes/deletes directory
    """
    # if the directory does not exist, try to create it
    if not os.path.isdir(path):
        #program_log.debug(f'Directory is not present. Creating {path}')
        try:
            os.makedirs(path)
        except Exception as e:
            program_log.error(f"Oof", print(e.__class__), "occurred")
            program_log.error(f"Unable to create dir at {path}")
            if debug:
                name = input("Any key to continue")
    else:
    # if the directory DOES exist, notify that we will be removing and
    # overwriting it
        if not clear:
            program_log.info(f'Directory is present, but we are deleting it anyway! {path}')
            program_log.info('clearing...')
        else:
            try:
                shutil.rmtree(path)
                os.makedirs(path)
            except Exception as e:
                program_log.error(f"Oof", print(e.__class__), "occurred")
                program_log.error(f"failed to clear directory: {path}")
                if debug:
                    name = input("Any key to continue")


def replace_in_file(old: str, new: str, path: str, debug: bool = False,
                    format="json"):
    """
    replaces a string inside target file
    regex function
    takes <old_value> <new_value> <path/to/old_value>
    """
    program_log.info(f"{old} --> {new}")
    full_path = path
    with open(full_path, 'r+') as f:
        text = f.read()
        text = re.sub(old, new, text)
        f.seek(0)
        f.write(text)
        f.truncate()


def quote(text: str):
    """
    returns a quoted variable
    quotes a variable
    """
    word = f'"{text}"'
    return word


def get_environment_vars(identitfier: str, env_vars: dict, debug=True,
                         format="json"):
    """
    reads and sets environment vars + str to bool conversion
    all environment variables are just interpreted as strings.
    this means we have to make sure we convert variables
    like TRUE, True, true etc.. to booleans when we find them
    """

    # new set of env vars
    new_vars = {}

    # for each env var, KEY => key
    for var in env_vars.keys():
        try:
            lower = str(var).lower()
            name = re.sub(identitfier, "", lower)
            new_vars[name] = os.getenv(var)
        except KeyError:
            print_pretty(f"Please set the environment variable {var}", debug,
                         format)

    # handle boolean conversion since all env vars are strings
    for var in new_vars:
        try:
            if new_vars[var] in ['True', "true", "yes","Yes"]:
                new_vars[var] = True
            else:
                if new_vars[var] in ['False', "false", "no","No"]:
                    new_vars[var] = False
        except KeyError:
            print_pretty(f"Please set the environment variable {var}", debug)

    return new_vars


class Variables(object):
    """
    ephemeral, human readable, stateful, json/yaml memory cache

    based on:
    stackoverflow.com/questions/2060972/subclassing-python-dictionary-to-override-setitem,

    attemptes to recreate C# getter/setter with an event listener:
    docs.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/using-properties
    https://docs.microsoft.com/en-us/dotnet/standard/events/
    """

    def __init__(self, settings):
        """
        Create a new memory cache
        """
        for item in settings:
            self.change_value(item, settings[item])


    def __setattr__(self, key, value):
        """
        ########################
        Event entrypoint
        custom events go in here
        ########################
        """

        ##
        # Diff Values
        ##
        debug = True
        format = "json"
        program_log.info(f"Requesting value change on key: {key}")
        self.diff_values(key, value, debug, format)

        ##
        # prompt for confirmation
        ##
        self.steppy()

        super(Variables, self).__setattr__(key, value)


    def change_value(self, key, value):
        """
        Changes the value of settings and logs the change using deepdiff
        alters the behaviro here as this will be the global entry point
        for manual action
        """
        debug = True
        format = "json"
        self.diff_values(key, value, debug, format)
        self.settings[key] = value


    def get_current_value(self, key, value, debug=False):
        """
        Returns the current value of a key. Utility function
        for diff_values
        """
        current_value = None

        for section in self.__dict__:
            if section == key:
                current_value = self.__dict__[section]

            for item in section:
                if item == key:
                    current_value = self.__dict__[section][item]

        # and finally, return
        return current_value


    def diff_values(self, key, value, debug=False, format="json"):
        """
        returns a diff between current and proposed state
        try to find the current value if it exists
        opitmization needed
        """
        current_value = self.get_current_value(key, value, debug)

        # actually do the diff
        diff_data = ""

        try:
            diff_data = DeepDiff(current_value, value, report_repetition=True, verbose_level=2, )
        except Exception:
            program_log.error(f"Unable to diff value: {current_value}")

        # generate the diff report
        data_string = (json.loads(diff_data.to_json()))

        # clean up the nested values
        diff_results =  {
            'old_type': f"{data_string['type_changes']['root']['old_type']}",
            'old_value':  f"{data_string['type_changes']['root']['old_value']}",
            'new_type': f"{data_string['type_changes']['root']['new_type']}",
            'new_value': print_pretty(f"{data_string['type_changes']['root']['new_value']}", debug, format)
        }

        #program_log.debug(print_pretty(data_string['type_changes']['root'], debug, format))


    def steppy(self):
        """
        If a settings names "go_steppy" is found in self.settings and is True,
        execution of tasks will pause upon memory item changes.
        """
        if "go_steppy" in self.__dict__:
            if self.go_steppy:
                name = input('Any Key to Approve')

