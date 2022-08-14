#!/usr/bin/python3

## Parses a SQLake Worksheet and executes each command using the Upsolver CLI ##
from inspect import FullArgSpec
import subprocess
from typing import NamedTuple
import json
import os
import sys
import getopt

class QueryResults (NamedTuple):
    order: int # order of exeuction
    query: str # query string
    out: str # output from the execution
    err: str # error from the execution

def main():
    worksheet_path = ''
    print('Starting to parse and execute worksheets')
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hw:')
        if not opts:
            print('executeworksheet.py -w <path_to_worksheet>')
            exit(2)
    except getopt.GetoptError:
        print('executeworksheet.py -w <path_to_worksheet>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('executeworksheet.py -w <path_to_worksheet>')
            sys.exit()
        elif opt == '-w':
            if os.path.exists(arg):
                worksheet_path = arg
            else:
                print('could not find a worksheet in the given path '+arg)
                sys.exit(2)
        else:
            print('No args found')
            sys.exit(2)
    
    files = getworksheets(worksheet_path)
    for file in files:
        sql_cmd = splitworksheet(file)
        c = 1
        results = []
        for cmd in sql_cmd:
            if c <= len(sql_cmd):
                try:
                    print('Executing {0}: {1}'.format(c, cmd))
                    res = subprocess.run(
                        ['upsolver', '-c', '~/.upsolver/config', 'execute', "{}".format(cmd)], capture_output=True, text=True, check=True
                    )
                    #print('Query results: {}'.format(res.stdout))
                    results.append(QueryResults(c, cmd, res.stdout, res.stderr))
                    c += 1
                except:
                    print('Query execution failed: {}'.format(res.stderr))
                    exit(2)

        print('Finished executing {} \r\n'.format(os.path.basename(file)))
        print(json.dumps(results))
        
## walk the input path
## return a list of .sql files (assumed to be worksheets)
def getworksheets(input_path):
    print('Looking for worksheets in {}'.format(input_path))
    worksheets = []
    for path, subdirs, files in os.walk(input_path):
        for name in files:
            fullpath = path + '/' + name
            print('full path: {}'.format(fullpath))

            name, file_ext = os.path.splitext(fullpath)
            if file_ext.lower() in ['.sql']:
                worksheets.append(fullpath)

    return worksheets

## read each worksheet, and split it on ;
## return a list of sql commands to execute
def splitworksheet(path):
    print('Spliting worksheet in {}'.format(path))
    cmds = []
    fd = open(path, 'r')
    ws_file = fd.read()
    fd.close()

    sql_commands = ws_file.split(';')
    
    for s in sql_commands:
        s = s.strip()
        if s:
            s = s + ';'
            cmds.append(s)

    return cmds

if __name__ == '__main__':
  main()