import os
import sys
import argparse
import re


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("logDir", help="Path to the log directory.")
    parser.add_argument("proprietariesDir", help="Path to the proprietaries directory.")
    return parser.parse_args(sys.argv[1:])


def find_unknown_sources(log_file):
    with open(log_file, "r") as f:
        unknownsources = re.findall(r"(?<=!!\s).+?(?=:\sfile not found in source)", f.read())
    return unknownsources


def delete_unknown_sources(proprietaries_file, unknown_sources):
    with open(proprietaries_file, "r") as f:
        proprietaries_lines = f.readlines()

    deleted_lines = []
    for num, line in enumerate(proprietaries_lines):
        for unknown_source in unknown_sources:
            if unknown_source in line:
                deleted_lines.append(num)
                print(f"Deleted: {unknown_source}")

    with open(proprietaries_file, "w") as f:
        for num, line in enumerate(proprietaries_lines):
            if num not in deleted_lines:
                f.write(line)


def main():
    args = parse_args()

    log_file = args.logDir
    proprietaries_file = args.proprietariesDir

    if not os.path.exists(log_file):
        print("Log file does not exist: {}".format(log_file))
        sys.exit(1)

    if not os.path.exists(proprietaries_file):
        print("Proprietaries file does not exist: {}".format(proprietaries_file))
        sys.exit(1)

    unknown_sources = find_unknown_sources(log_file)
    delete_unknown_sources(proprietaries_file, unknown_sources)


if __name__ == "__main__":
    main()

