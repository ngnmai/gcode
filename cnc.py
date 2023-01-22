'''
Assignment: G-Code interpreter 
User: Mai Nguyen 
Description: 
Implement a program that reads the attached G-Code program from a file and parses the instructions. 
The program is expected to call MachineClient's stub methods to simulate execution. 
MachineClient implements a simplified interface to control a CNC machine.
'''

import sys


#inputfile
inFile = sys.argv[1]
with open(inFile, 'r') as f:
    gcode = f.read()

print(gcode)
print(type(gcode))

prorgammStatus = False 
cmdDict = {}

def filtering(gcode_line):
    '''
    param gcode_line: a string, containing 1 gcode line in a programme
    return: type of gcode
    "0" = initialisation code
    "1" = comment
    "2" = program number
    "3" = gcode to be interpreted
    '''
    if gcode_line.find('%') != -1:
        return 0
    elif gcode_line.find('(') != -1: 
        return 1
    elif gcode_line.find('o')!= -1 or gcode_line.find('O')!= -1:
        return 2
    else:
        return 3

def startingProgramm(flag = True):
    prorgammStatus = True

def commenting(cmt):
    cmt = cmt.replace('(', '')
    cmt = cmt.replace(')', '')
    return str("COMMENT: " + cmt)

def programmInfo(no):
    '''
    param no: a string, gcode line of programme number 
    return: 1st -> number of programm (int)
            2nd -> programm numbe in gcode
    '''
    num = no.replace('o', '')
    return int(num), no

def preppingLine(line):
    cmd_s = line.split()
    index = int(cmd_s[0][1:])
    cmdDict[index] = cmd_s[1:]


def getLine(gcode_line):
    '''
    param gcode_line: a string, containing 1 gcode line in a programme
    return: list, including words in gcode line separating by a space
    '''

class MachineClient:


def main():
    #getting lines
    gcode_Lines = f.readlines() #a list of gcode lines 
    for gcode_Line in gcode_Lines:
        type_ = filtering(gcode_Line)

