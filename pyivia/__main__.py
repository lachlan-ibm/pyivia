#!/usr/bin/env python3

import argparse
import logging
import pyivia
import inspect
import json
import getpass

logger = logging.getLogger("pyivia")
cli_config = { 
    'json_format' : True
}

def get_functions(obj):
    r"""
    Get functions from the obj that can be called via the CLI
    """
    results = { }

    for obj_type in type(obj).__mro__:
        if obj_type == object:
            continue

        type_dict = obj_type.__dict__

        for name, value in type_dict.items():
            if not name.startswith("_") and callable(value):
                if name not in results:
                    results[name] = (value, inspect.signature(value))
    
    return results

def is_usable_attribute(name, value):
    r"""
    Is the attribute something we want to use in the CLI
    """
    if name.startswith("_"):
        # Don't use 'private' variables
        return False
    elif value is None:
        # Can't do much with null values
        return False
    elif type(value) == str or type(value) == pyivia.util.restclient.RESTClient:
        # Don't try to work with these value types
        return False
    else:
        # Everything else is fine to use
        return True
    

def get_attributes(obj):
    r"""
    Get attributes from the obj that can be accessed via the CLI
    """
    attrs = { }
    for name,value in obj.__dict__.items():
        if is_usable_attribute(name, value):
            attrs[name] = value

    return attrs

def is_blank(value):
    r"""
    Is the value blank
    """
    return value is None or len(value) == 0 or value.isspace()

def parse_value(value):
    r"""
    Parse a value provided on the command line into an appropriate type.
    """
    try:
        # This should handle all data types except string
        return json.loads(value)
    except:
        # It's a string
        return value

def parse_param(param):
    r"""
    Parse a parameter into a name (if specified) and a value.
    """
    name = None
    value = None

    parts = param.split("=", 2)
    if len(parts) == 2:
        name = parts[0]
        value = parts[1]
    else:
        value = param

    return name,parse_value(value)


def parse_args(object, signature, remaining_params):
    r"""
    Parse the remaining command line arguments into function parameters.
    """
    args = [object]
    kwargs = { }

    unnamed_params = []
    named_params = {}

    for param in remaining_params:
        if is_blank(param):
            continue

        param_name, param_value = parse_param(param)
        if param_name in signature.parameters:
            named_params[param_name] = param_value
        else:
            # Not a known parameter, assume it's just a value with an equals sign in it.
            unnamed_params.append(parse_value(param))

    for name in signature.parameters.keys():
        if name == "self":
            continue

        if name in named_params:
            kwargs[name] = named_params[name]
        else:
            if len(unnamed_params) > 0:
                kwargs[name] = unnamed_params[0]
                unnamed_params = unnamed_params[1:]
            else:
                logger.debug(f"Cannot find something to bind to {name}")

    return signature.bind(*args, **kwargs)

def is_response(obj):
    r"""
    Does the object represent a response that should be displayed?
    """
    return type(obj) == pyivia.util.model.Response or \
        type(obj) == bool or type(obj) == str

def display_response(result):
    r"""
    Display the response.
    """
    if (type(result) == pyivia.util.model.Response):
        print(f"Status: {result.status_code}")
        if result.json is not None:
            if cli_config['json_format']:
                print(json.dumps(result.json, indent=4))
            else:
                print(result.json)
    else:
        print(result)

def print_signature(signature):
    r"""
    Print the method signature in a manner that is more relevant to the CLI
    """
    signature_str = str(signature)
    self_prefix = "(self, "
    if signature_str == "(self)":
        print("()")
    elif signature_str.startswith(self_prefix):
        print("(" + signature_str[len(self_prefix):])



def run_command(object, method, signature, cmd_string, remaining_params):
    r"""
    Run a command and print the result
    """
    if len(remaining_params) > 0 and remaining_params[-1] == "-?":
        print(cmd_string)
        print_signature(signature)
        if method.__doc__ is not None:
            print(method.__doc__)
    else:
        try:
            bound_args = parse_args(object, signature, remaining_params)
            result = method(*bound_args.args, **bound_args.kwargs)
            if is_response(result):
                display_response(result)
            else:
                print(result)
        except Exception as e:
            print(f"{e}")
    

def print_cmd_usage(cmd):
    r"""
    Print the usage for a command, showing what can be done with it
    """
    funcs = get_functions(cmd)
    attrs = get_attributes(cmd)
    all_options = sorted(list(funcs.keys()) + list(attrs.keys()))

    print("Possible options are:")
    print("    " + "\n    ".join(all_options))


# The main line

parser = argparse.ArgumentParser("pyivia")
parser.add_argument("-v", "--verbose", help="Enable verbose logging", action="store_true", default=False)
parser.add_argument("-b", "--base_url", help="IVIA Base URL", required=True)
parser.add_argument("-u", "--username", default="admin", help="Username")
parser.add_argument("-p", "--password", default=None, help="Password")
parser.add_argument("--json-format", default=True, dest="json_format", action="store_true", help="Apply formatting to JSON output.")
parser.add_argument("--no-json-format", dest="json_format", action="store_false", help="Do not apply formatting to JSON output.")
parser.add_argument("command", nargs=argparse.REMAINDER, help="Command")

args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

password = args.password
if password is None:
    password = getpass.getpass()

appliance = pyivia.Factory(args.base_url, args.username, password)
current_obj = appliance

ran_cmd = False

cli_config['json_format'] = args.json_format

for idx,cmd in enumerate(args.command):
    logger.debug(f"Processing command [{cmd}]")
    if is_blank(cmd):
        continue

    if not callable(current_obj):
        functions = get_functions(current_obj)
        func, sig = None, None
        for name in [cmd, f"get_{cmd}" ]:
            if name in functions:
                (func, sig) = functions[name]
                break
        
        if func is not None:
            if len(sig.parameters) == 1:
                result = func(current_obj)
                if is_response(result):
                    display_response(result)
                    ran_cmd = True
                    break
                else:
                    current_obj = func(current_obj)
            else:
                run_command(current_obj, func, sig, " ".join(args.command[0:idx+1]), args.command[idx+1:])
                ran_cmd = True
                break

        else:
            attrs = get_attributes(current_obj)
            if cmd in attrs:
                current_obj = attrs[cmd]
            elif cmd == "-?":
                print_cmd_usage(current_obj)
                ran_cmd = True
                break
            else:
                logger.error(f"Could not find how to handle {cmd}")
                break

if not ran_cmd:
    print_cmd_usage(current_obj)