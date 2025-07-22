#!/usr/bin/env python3


import argparse
import logging
import os
import pyivia
import inspect

logger = logging.getLogger(__name__)


def get_functions(obj):
    type_dict = type(obj).__dict__

    results = { }

    for name, value in type_dict.items():
        if not name.startswith("_") and callable(value):
            results[name] = (value, inspect.signature(value))
    return results

def get_attributes(obj):

    attrs = { }
    for name,value in obj.__dict__.items():
        if not name.startswith("_") and value is not None and type(value) != str:
            attrs[name] = value
    return attrs

def parse_value(value):
    logger.debug(f"Parsing value: {value}")
    if value.startswith("[") and value.endswith("]"):
        value = eval(value)
    return value

def parse_param(param):
    name = None
    value = None

    parts = param.split("=", 2)
    if len(parts) == 2:
        name = parts[0]
        value = parts[1]
    else:
        value = param

    value = parse_value(value)
    return name,value



def parse_args(object, signature, remaining_params):
    args = [object]
    kwargs = { }

    unnamed_params = []
    named_params = {}

    for param in remaining_params:
        if param is None or len(param) == 0 or param.isspace():
            continue

        param_name, param_value = parse_param(param)
        if param_name in signature.parameters:
            named_params[param_name] = param_value
        else:
            unnamed_params.append(parse_value(param))

    for name,value in signature.parameters.items():
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


def run_command(object, method, signature, remaining_params):
    try:
        bound_args = parse_args(object, signature, remaining_params)
        result = method(*bound_args.args, **bound_args.kwargs)
        print(f"{result}")
    except:
        print(f"Did not get required parameters: {signature}")

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Enable verbose logging", action="store_true", default=False)
parser.add_argument("-b", "--base_url", help="IVIA Base URL", required=True)
parser.add_argument("-u", "--username", default="admin", help="Username")
parser.add_argument("-p", "--password", default="admin", help="Password")
parser.add_argument("command", nargs=argparse.REMAINDER, help="Command")

args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

appliance = pyivia.Factory(args.base_url, args.username, args.password)
cmd_stack = [appliance]

ran_cmd = False

for idx,cmd in enumerate(args.command):
    logger.debug(f"Processing command [{cmd}]")
    current = cmd_stack[-1]

    if not callable(current):
        functions = get_functions(current)
        func, sig = None, None
        for name in [cmd, f"get_{cmd}" ]:
            if name in functions:
                (func, sig) = functions[name]
                break

        if func is not None:
            if len(sig.parameters) == 1:
                cmd_stack.append(func(current))
            else:
                run_command(current, func, sig, args.command[idx+1:])
                ran_cmd = True
                break
                break
        else:
            attrs = get_attributes(current)
            if cmd in attrs:
                cmd_stack.append(attrs[cmd])
            else:
                logger.error(f"Could not find how to handle {cmd}")
                break

if not ran_cmd:
    funcs = get_functions(cmd_stack[-1])
    attrs = get_attributes(cmd_stack[-1])
    all_options = sorted(list(funcs.keys()) + list(attrs.keys()))
    all_options_str = "\n    ".join(all_options)
    print("Could not find a command to run. Possible options are:")
    print(f"    {all_options_str}")
