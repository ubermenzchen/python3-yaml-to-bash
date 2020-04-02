#!/usr/bin/env python3

from sys import stdin, stderr, stdout, exit, argv
from yaml import load, SafeLoader
from getopt import getopt, GetoptError
from json import dumps

try:
    options, remainder = getopt(argv[1:], 'f:s', ['stdin', 'space', 'field='])
except GetoptError as err:
    stderr.write('ERROR: %s\n' % err)
    exit(1)

stdin_flag = False
field_flag = False

fields = []
sep = '\n'

for opt, arg in options:
    if opt in ('--stdin', '-s'):
        stdin_flag = True
    elif opt in ('--field', '-f'):
        field_flag = True
        fields.append(arg)
    elif opt in ('--space'):
        sep = ' '

if not field_flag:
    stderr.write('ERROR: %s\n' % 'Please provide fields to show')
    exit(1)

string = ''

if stdin_flag:
    string += stdin.read()
else:
    with open(remainder[0], 'r') as f:
        string += f.read()

obj = load(string, Loader=SafeLoader)

for field in fields:
    s = field.strip().split('.')
    p = obj
    for i in s:
        p = p[i]
    stdout.write('%s%c' % (dumps(p), sep))
