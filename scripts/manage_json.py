# JSON management command line utility with interactive mode

import json
import os
import sys
import argparse
import re

# move all json files in current directory to subdirectory json
def move_json_files():
    os.system("mkdir json")
    os.system("mv *.json json")

# combine all json files in current directory into one file
def combine_json_files(filename):
    os.system(f"cat *.json > {filename}")

# get all comments from a json file
def get_comments(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="Manage json files")
    parser.add_argument("-m", "--move", action="store_true", help="Move all json files in current directory to subdirectory json")
    parser.add_argument("-c", "--combine", action="store_true", help="Combine all json files in current directory into one file")
    parser.add_argument("-g", "--get", action="store_true", help="Get all comments from a json file")
    parser.add_argument("-f", "--filename", type=str, help="Filename of json file")
    args = parser.parse_args()

    # move json files
    if args.move:
        move_json_files()

    # combine json files
    if args.combine:
        combine_json_files(args.filename)

    # get comments from json file
    if args.get:
        comments = get_comments(args.filename)
        print(comments)