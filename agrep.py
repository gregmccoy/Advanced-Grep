import os
import re
import argparse
from subprocess import call

def file_match(fname, pat):
    try:
        f = open(fname, "rt", errors="ignore")
    except IOError:
        return
    data = f.readlines()
    f.close()
    print(fname)

    for i, line in enumerate(data):
        if pat.search(line):
            return True
    return False

def edit(fname, pat):
    try:
        f = open(fname, "rt", errors="ignore")
    except IOError:
        return

    data = f.readlines()

    f.close()
    for i, line in enumerate(data):
        if pat.search(line):
            print("Line Number: " + str(i))
            print("\nFile:")
            print(fname)
            print("\nLine:")
            print(line)
            print("Edit (y/n)")
            user_response = input()
            if user_response == 'y':
                user_response = input("Checkout first? (y/n)")
                if user_response == 'y':
                    call(["git", "checkout", "staging", fname])
                    print(fname)
                    input()
                call(["vim", fname])
            call(["clear"])

def grep(dir_name, s_pat):
    s_pat = str(s_pat)
    pat = re.compile(s_pat)
    fulltree = {}
    found = 0
    os.chdir(dir_name)
    for dirpath, dirnames, filenames in os.walk("."):
        for i, fname in enumerate(filenames):
            fullname = os.path.join(dirpath, fname)
            if file_match(fullname, pat):
                fulltree[str(found)] = fullname
                found += 1

    for key, value in fulltree.items():
        call(["clear"])
        print("File " + str(key) + " of " + str(len(fulltree)))
        edit(value, pat)

def sources(path):
    grep(path, input("Search: "))

#Check for command line
parser = argparse.ArgumentParser()
parser.add_argument(dest='input', help="Enter folder to search")
args = parser.parse_args()
sources(args.input)

