import os
import sys
import argparse
import re


lines = []
ln = []


def create_arg_parser():
    # Creates and returns the ArgumentParser object

    parser = argparse.ArgumentParser()
    parser.add_argument("logDir", help="Path to the log directory.")
    parser.add_argument("proprietariesDir", help="Path to the proprietaries directory.")
    return parser


arg_parser = create_arg_parser()
parsed_args = arg_parser.parse_args(sys.argv[1:])
f1 = parsed_args.logDir
f2 = parsed_args.proprietariesDir


if os.path.exists(f1):
    print("Log file found, try to read it!")
    with open(f1, "r") as file:
        unknownsources = (re.findall(r"(?<=!!\s).+?(?=:\sfile not found in source)", file.read()))


with open(f2, "r") as file:
    ln = file.readlines()


with open(f2, "r") as file:
    for num, line in enumerate(file):
        for unknownsource in unknownsources:
            if unknownsource in line:
                lines.append(num)
                print(f"deleted: {unknownsource}")


with open(f2, "w") as file:
    for num, line in enumerate(ln):
        if num not in lines:
            file.write(line)