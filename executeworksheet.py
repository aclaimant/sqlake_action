#!/usr/bin/python3

## Parses a SQLake Worksheet and executes each command using the Upsolver CLI ##
import subprocess
from typing import NamedTuple
import json
import os
import re
import sys
import getopt

class QueryResults (NamedTuple):
    worksheet: str # worksheet path and name
    order: int # order of exeuction
    query: str # query string
    out: str # output from the execution
    err: str # error from the execution

def main():
    worksheet_path = ''
    local_path = ''
    print('Starting to parse and execute worksheets')

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hw:o:')
        print('**args {}'.format(args))
        if not opts:
            print('executeworksheet.py -w <path_to_worksheet> -o <output_path>')
            exit(2)
    except getopt.GetoptError:
        print('executeworksheet.py -w <path_to_worksheet> -o <output_path>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('executeworksheet.py -w <path_to_worksheet> -o <output_path>')
            sys.exit()
        elif opt == '-w':
            if os.path.exists(arg):
                worksheet_path = arg
            else:
                print('could not find a worksheet in the given path '+arg)
                sys.exit(2)
        elif opt == '-o':
            if os.path.exists(arg):
                local_path = arg
            else:
                print('you must provide an output path to write the results of queries')
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
                        ['upsolver', '-c', '/config', 'execute', "{}".format(cmd)], capture_output=True, text=True, check=True
                    )
                    results.append(QueryResults(file, c, cmd, res.stdout, res.stderr))
                    c += 1
                except subprocess.CalledProcessError as e:
                    print('Query execution failed: {}'.format(e.stderr))
                    results.append(QueryResults(file, c, cmd, '', e.stderr))
                    exit(2)

        print('Finished executing {} \r\n'.format(os.path.basename(file)))
        #print(json.dumps(results))
        writeresults(results, local_path)
        
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
        re.sub(r'(?m)^ *\-\-.*\n?', '', s)
        if s:
            s = s + ';'
            cmds.append(s)

    return cmds

## write the worksheet execution results to a temp file
def writeresults(data, local_path):
    print('Writing execution results to {}'.format(local_path))
    md = formatoutput(data)
    with open(local_path + '/worksheet_output.md', 'a', encoding='utf-8') as fd:
        fd.write(md)

def formatoutput(data):
    output = '## Upsolver SQLake Worksheet Execution Summary \r\n\r\n'
    for i in data:
        output += '### **{}** \r\n\r\n'.format(i.worksheet)
        output += '--- \r\n\r\n'
        output += '**Query position in Worksheet:** {} \r\n\r\n'.format(i.order)
        output += '**Query text:** `{}` \r\n\r\n'.format(i.query)
        output += '**Query results:** `{}` \r\n\r\n'.format(i.out)
        output += '**Errors:** `{}` \r\n\r\n'.format(i.err)

    return output

if __name__ == '__main__':
  main()