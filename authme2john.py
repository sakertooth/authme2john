#!/usr/bin/python
import sys
import os

def convert(password):
    password = password.strip('\'')
    if password.startswith("$SHA$") is False:
        print("Invalid Token: Does not begin with $SHA$")
        exit(1)

    password = password[5:]
    salthash = password.split('$')
    
    if len(salthash) != 2:
        print("Invalid Token: Could not get salt and/or hash correctly.")
        exit(1)
    elif len(salthash[0]) != 16 or len(salthash[1]) != 64:
        print("Invalid Token: Bad salt/hash lengths.")
        exit(1)

    return f'{salthash[1].strip()}${salthash[0]}'


if len(sys.argv) < 2:
    print("Usage: authme2john.py <single/file> [OUTPUT]")
    print("(Does the file exist, or is the hash not single-quoted?)")
    exit(1)

password = sys.argv[1]
output = sys.argv[2] if len(sys.argv) == 3 and os.path.isfile(sys.argv[2]) else None

if os.path.isfile(password):
    ostream = None
    if output is not None:
        ostream = open(output, 'a')

    for hash in open(password, 'r'):
        if output is None:
            print(convert(hash))
        else:
           ostream.write(convert(hash) + "\n")
           
    if ostream is not None:
        ostream.close()
else:
    print(convert(password))
