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
    gcode_Lines = f.readlines()

programmStatus = False 


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

def startingProgramm(flag = True, value = "Unnamed"):
    programmStatus = True
    print("Starting programm number : {}".format(value))

def endingProrgamm():
    programmStatus = False
    print("End of programm")

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
    commands = cmd_s[1:]
    return index, commands


def getLine(gcode_line):
    '''
    param gcode_line: a string, containing 1 gcode line in a programme
    return: list, including words in gcode line separating by a space
    '''
    return 

class MachineClient:
    def _init_(self, x_cor = 0, y_cor = 0, z_cor = 0, name= "Unnamed"):
        self.name_prog = name
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.z_cor = z_cor
        self.tool = None
        self.feed_rate = 0
        self.spindle_speed = 0
        self.coolant_status = False

    def home(self):
        ''' 
        Moving the machine back to home position
        '''
        self.x_cor, self.y_cor, self.z_cor = 0, 0, 0
        print("Moving to home.")

    def move(self, x, y, z):
        '''
        Move spindle to given coordinates
        '''
        self.x_cor, self.y_cor, self.z_cor = x, y, z
        print("Moving to X={:.3f}, Y={:.3f}, Z={:.3f} [mm]".format(x, y, z))


    def move_x(self, value):
        '''
        Move spindle to given X_coordinate. 
        Unchanged Y_Coordinate and Z_Coordinate
        '''
        self.x_cor = value 
        print("Moving X to {:.3f} [mm].".format(value))
    
    def move_y(self, value):
        '''
        Move spindle to given Y_coordinate. 
        Unchanged X_Coordinate and Z_Coordinate
        '''
        self.y_cor = value 
        print("Moving Y to {:.3f} [mm].".format(value))

    def move_z(self, value):
        '''
        Move spindle to given Z_coordinate. 
        Unchanged X_Coordinate and Y_Coordinate
        '''
        self.z_cor = value 
        print("Moving Z to {:.3f} [mm].".format(value))
    
    def set_feed_rate(self, value):
        self.feed_rate = value
        print("Using feed rate {} [mm/s].".format(value))
    
    def set_spindle_speed(self, value):
        self.spindle_speed = value
        print("Using spindle speed {} [mm/s].".format(value))
    
    def set_tool_name(self, tool_name):
        self.tool = tool_name

    def change_tool(self, tool_name):
        print("Changing tool '{:.s}'.".format(tool_name))
    
    def coolant_on(self):
        self.coolant_status = True
        print("Coolant turned on.")

    def coolant_off(self):
        self.coolant_status = False
        print("Coolant turn off.")


def main():
    #prepping
    for gcode_Line in gcode_Lines:
        type_ = filtering(gcode_Line)
        print(type_)
        if type_ == 0:
            pass
        if type_ == 1:
            commenting(gcode_Line)
        if type_ == 2:
            prog_num, gcode_num = programmInfo(gcode_Line)
            startingProgramm(True, prog_num)
        if type_ == 3: 
            index, cmds = preppingLine(gcode_Line)
            if index == "N1":
                pass
            else:
                pass


main()