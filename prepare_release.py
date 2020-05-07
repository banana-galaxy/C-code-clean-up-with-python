#!/usr/bin/env python3

from sys import argv
import shutil
import os

starts = ["#if ", "#if\n", "#ifdef ", "#ifdef\n"]
start_print = ["#if", "#ifdef"]
end = "#endif"
check = "TA_CALIBRATION"

def short_help():
    print(f'''Usage: ./prepare_release [SOURCE DIRECTORY]
''', end="")

if len(argv) == 1:
    short_help()
    print("Error: No source directory given")
    quit()

folder = argv[1]
destination = f"{argv[1]}/release"
forbbiden_list = [f"{folder}/prepare_release.py", f"{folder}/.git", f"{folder}/release"]

def print_help():
    global starts
    print(f'''
prepare_release help

prepare_release copies everything from a given directory to a directory called "release" that it creates inside the given one
while copying it checks for files that have the word "{check}" inside them and deletes the code they have inbetween a starting word: ''', end="")
    for start in start_print:
        print(f'"{start}" ', end="")
    print(f'''and an end word: "{end}"\nthe words ''', end="")
    for start2 in start_print:
        print(f'"{start2}", ', end="")
    print(f'''"{end}", and "{check}"" are all defined in variables at the top of the code

Usage: ./prepare_release [SOURCE DIRECTORY]
''', end="")

def check_code(path, check):
    with open(path, "r") as f:
        for line in f:
            if check in line:
                return True
    return False

def check_file(path):
    isfile = False

    try:
        with open(path, 'r') as f:
            pass
        isfile = True
    except IsADirectoryError:
        pass
                
    return isfile

def main_code(directory):
    global folder, destination
    global check, starts, end
    dirs = os.listdir(directory)
    for instance in dirs:

        path = f"{directory}/{instance}"
        pure = path.split(folder)[1]
        new_path = destination + pure
        exists = False

        if os.path.exists(new_path):
            user = input(f"{new_path} already exists, continue anyway? Continuing will completely rewrite it [y/N] ")
            if user != "y" and user != "Y":
                quit()
            else:
                exists = True

        if not path in forbbiden_list:
            if os.path.isdir(path):
                if exists:
                    shutil.rmtree(new_path)
                os.mkdir(new_path)
                main_code(path)

            elif check_file(path):
                if exists:
                    os.remove(new_path)
                if check_code(path, check):
                    lines = []
                    with open(path, "r") as f:
                        count = 0
                        for line in f:
                            for start in starts:
                                if line.startswith(start):
                                    count += 1
                            if count <= 0:
                                count = 0
                                lines.append(line)
                            if line.startswith(end):
                                count -= 1
                    if count > 0:
                        print(f'an "#if" or "#ifdef" is not closed in {path}')
                        quit()
                    new_lines = ""
                    for line in lines:
                        new_lines += line
                    # writing to file copy
                    with open(new_path, "w") as f:
                        f.write(new_lines)
                else:
                    shutil.copyfile(path, new_path)

if folder == "--help" or folder == "-H":
    print_help()
    quit()

if not os.path.exists(destination):
        os.mkdir(destination)
else:
    user = input(f"{destination} already exists, continue anyway? [y/N] ")
    if user != "y" and user != "Y":
        quit()

short_help()
main_code(folder)