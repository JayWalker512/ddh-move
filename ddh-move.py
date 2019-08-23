#!/usr/bin/env python3

import os
import sys
import time
import json

def move_files(list_of_files, destination_path):
    for file in list_of_files:
        os.rename(file, destination_path + "/" + os.path.basename(file))


def move_dupes(lists_of_dupes, destination):
    list_of_files_to_move = []
    for element in lists_of_dupes:
        keep, move = split_first_by_alpha(element) #need to parameterize move conditional somehow
        move_files(move, destination)


def split_first_by_alpha(list_of_strings):
    sorted_list = sorted(list_of_strings)
    return sorted_list[:1], sorted_list[1:]


def get_lists_of_dupes(ddh_json):
    lists_of_dupes = []
    for result_dict in ddh_json: #the outermost element of the json is a list
        if len(result_dict['file_paths']) > 1:
            lists_of_dupes.append(result_dict['file_paths'])

    return lists_of_dupes


def get_json(in_str):
    json_dict = {}
    try:
        json_dict = json.loads(in_str)
    except (json.JSONDecodeError) as e:
        return None
    return json_dict


def get_options_dict(arguments):
    options = {'dry-run': False}
    if len(arguments) < 2:
        return None

    if os.path.exists(arguments[1]):
        options['destination'] = arguments[1]
    else:
        return None

    if len(arguments) == 3 and arguments[2] == "--dry-run":
        options['dry-run'] = True
    elif len(arguments) == 3:
        return None

    return options


def print_help():
    help_string = """USAGE:
    ddh-move.py <Destination> [OPTIONS]
OPTIONS:
    --dry-run\tPrint the files to be moved without moving them."""

    print(help_string)


def get_stdin_string():
    buff = []
    while True:
        try:
            line = sys.stdin.read(1)
            if line == "":
                break
        except (KeyboardInterrupt, EOFError, Exception) as e:
            sys.stdout.flush()
            print(e)
            print(sys.exc_info())
            break
        buff.append(line)
        if line == "\n":
            sys.stdout.flush()

    in_str = "".join(buff)
    return in_str


def main(argv):
        options = get_options_dict(argv)
        if options is None:
            print_help()
            sys.exit(1)

        json_dict = get_json(get_stdin_string())
        lists_of_dupes = get_lists_of_dupes(json_dict)
        if options['dry-run']:
            for element in lists_of_dupes:
                keep, move = split_first_by_alpha(element)
                for file in move:
                    print(file)
        else:
            move_dupes(lists_of_dupes, options['destination'])

        sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)