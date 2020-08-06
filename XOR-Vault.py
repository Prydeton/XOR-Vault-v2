#!/usr/local/bin/python3
import sys
import os
import argparse

def read(path):
    if not os.path.isfile(path):
        print("No file found in path " + path)
        sys.exit(1)
    file = open(path, 'r')
    return file.read()

def write(value, path):
    if not os.path.isfile(path):
        print("No file found in path " + path)
        sys.exit(1)
    file = open(path, 'w')
    file.write(value)

def convert_to_binary(part_passcode):
    binary_code = ""
    for number in list(part_passcode):
        part_binary_code = bin(int(number))[2:].zfill(4)
        binary_code += part_binary_code
    return binary_code

def XOR(binary1, binary2):
    answer = ""
    for i in range(0, len(binary1)):
        answer += str(int(binary1[i]) ^ int(binary2[i]))
    return answer

def input_passcodes():
    passcode = ""
    for i in range(1,4):
        part_passcode = input("Please enter passcode " + str(i) + "/3: ")
        if not part_passcode.isnumeric or len(part_passcode) != 5:
            print("Invalid passcode - Passcode must be 5 digits and numerical.")
            sys.exit(1)
        part_passcode = convert_to_binary(part_passcode)
        if passcode == "":
            passcode = part_passcode
        else:
            passcode = XOR(passcode, part_passcode)
    return passcode

parser = argparse.ArgumentParser(description = "Configure or access 3 passcode lock")
command_group = parser.add_mutually_exclusive_group()
command_group.add_argument('-a', '--access', help="Access the lock (Default)", action='store_true')
command_group.add_argument('-c', '--configure', help="Configure the lock", action='store_true')
args = parser.parse_args()

binary_passcode = input_passcodes()
if args.configure:
    write(binary_passcode, os.getcwd() + "/masterkey.txt")
    print("Safe is ready to use")
else:
    if binary_passcode == read(os.getcwd() + "/masterkey.txt"):
        print("Correct password entered - Safe unlocked")
    else:
        print("Invalid password entered - Safe not unlocked")