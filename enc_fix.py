#!/usr/bin/env python
# -*- coding: utf-8 -*-

# enc_fix - checks that file is UTF-8 encoded and fix if not.
#
# If file isn't in UTF-8 or partitly, script converts
# file using ex (vim) editor.
# You may see results in `pre-commit.git.log` file.
#
# Dependencies: vim
#
# Usage:
# Simply put this script in project root folder and run:
#
# $> ./enc_fix.git.py "`find . -type f -print | egrep -v '\.git|mp3|<file_extension_to_exclude>'`" > enc_fix.git.log


import re
import sys
import os.path
from subprocess import call


def file_ck(f,ENC):
    failed = 0
    with open(f, 'rb') as fh:
        print "encck: Handling file: %s" % f
        # Line number in file (if error occurs)
        nl = 1

        for line in fh:
            # rstrip - strip linebreaks
            line = line.rstrip()

            # Exclude SQL comment lines
            if line.startswith('--'):
                line = str(next(fh, None)).rstrip()
                nl+=1

            # Exclude SQL comment multilines
            if line.startswith('/*'):
                while not line.endswith('*/'):
                    line = str(next(fh, None)).rstrip()
                    nl+=1
                line = str(next(fh, None)).rstrip()
                nl+=1

            if enc_ck(line,nl,ENC):
                failed = 1

            nl+=1

        if failed == 1:
            global wrong_files
            wrong_files.append(f)

    fh.close()
    print "\n"
    return


def enc_ck(line,nl,ENC):
    # Checks for unicode accordance.
    try:
        line.decode(ENC)
    except Exception as e:
        err_found(nl,e)
        return 1
    return


def err_found(nl,e=False):
    print "encck: Error in line %s:" % nl
    if e: print "encck:   %s\n" % e

    global wrong_encoding
    wrong_encoding = True

    return


def fix_file(f):
    return call(["ex", "-s", f, "-c e ++enc=cp1251", "-c w ++enc=utf8", "-c q"])


if __name__=="__main__":
    ENC = "utf-8" # encoding for checking
    EXT = "sql"   # file extension that should be check out

    global wrong_files
    wrong_files = []

    global wrong_encoding
    wrong_encoding = False

    files = sys.argv[1].split('\n')

    for f in files:
        # Check for file extension.
        # if not EXT in os.path.splitext(f)[-1]:
        #     continue

        if os.path.isfile(f):
            # Check file enconding
            file_ck(f,ENC)
        else:
            print "encck: Skip file. File is absent, maybe it was deleted: %s" % f


    if wrong_files:
        print "encck: Wrong files are:"
        for f in wrong_files:
            print f

            # Convert file using ex editor.
            if fix_file(f) == 0:
                print "       (Fixed)\n"
            else:
                print "       (ERROR while fixing)\n"
    else:
        print "encck: There is a no wrong files. All fine!"

