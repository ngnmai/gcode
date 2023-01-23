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
    print("Starting programm number : {}\n".format(value))

def endingProrgamm():
    programmStatus = False
    print("End of programm\n")

def commenting(cmt):
    cmt = cmt.replace('(', '')
    cmt = cmt.replace(')', '')
    return str("COMMENT: " + cmt + "\n")

def programmInfo(no):
    '''
    param no: a string, gcode line of programme number 
    return: 1st -> number of programm (int)
            2nd -> programm numbe in gcode
    '''
    num = no.replace('o', '')
    num = num.replace('O', '')
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
    def _init_(self,name):
        self.name_prog = name
        self.x_cor = 0
        self.y_cor = 0
        self.z_cor = 0
        self.x_prime = 0
        self.y_prime = 0
        self.z_prime = 0
        self.tool = None
        self.feed_rate = 0
        self.spindle_speed = 0
        self.coolant_status = False

    def home(self):
        ''' 
        Moving the machine back to home position
        '''
        self.x_cor, self.y_cor, self.z_cor = 0, 0, 0
        print("Moving to home.\n")

    def set_work_offset(self):
        print("Moving to offset coordinates. Setting this as (0,0,0).\n")

    def set_positioning_method(self, flag):
        if flag == 1:
            print("Setting positioning method as Increment.\n")
        else: 
            print("Setting positioning method as Absolute.\n")

    def set_prime_coordinate(self, xprime = 0, yprime = 0, zprime = 0):
        '''
        Setting the next destination coordinates
        '''
        self.x_prime, self.y_prime, self.z_prime = xprime, yprime, zprime

    def move(self):
        '''
        Move spindle to given coordinates
        '''
        self.x_cor, self.y_cor, self.z_cor = self.x_prime, self.y_prime, self.z_prime
        print("Moving to X={:.3f}, Y={:.3f}, Z={:.3f} [mm]\n".format(self.x_cor, self.y_cor, self.z_cor))

    def move_rapid(self):
        '''
        Move as fast as possible to a specified coordinate position
        '''
        self.x_cor, self.y_cor, self.z_cor = self.x_prime, self.y_prime, self.z_prime
        print("Moving rapidly to X={:.3f}, Y={:.3f}, Z={:.3f} [mm]\n".format(self.x_cor, self.y_cor, self.z_cor))

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
        print("Using feed rate {} [mm/s].\n".format(value))
    
    def set_spindle(self):
        print("Spindle on Clockwise\n")
    
    def stop_spindle(self):
        self.spindle_speed = 0
        print("Spindle stop\n")

    def set_spindle_speed(self, value):
        self.spindle_speed = value
        print("Using spindle speed {} [mm/s].\n".format(value))
    
    def set_tool_name(self, tool_name):
        self.tool = tool_name

    def change_tool(self):
        print("Changing tool '{:.s}'.\n".format(self.tool))
    
    def coolant_on(self):
        self.coolant_status = True
        print("Coolant turned on.\n")

    def coolant_off(self):
        self.coolant_status = False
        print("Coolant turn off.\n")

    def creating_dict_forMC(self):
        gcDict ={'T': {1 : self.set_tool_name(1)},
                    'M': {3 : self.set_spindle(),
                          5 : self.stop_spindle(), 
                          6 : self.change_tool(),
                          9 : self.coolant_off()},
                    'G': {54 : self.set_work_offset(),
                          90 : self.set_positioning_method(0), 
                          91 : self.set_positioning_method(1)}}
        return gcDict
                      
def main():
    #prepping
    for gcode_Line in gcode_Lines:
        type_ = filtering(gcode_Line)
        print(type_)
        actionList = {}
        if type_ == 0:
            pass
        if type_ == 1:
            commenting(gcode_Line)
        if type_ == 2:
            prog_num, gcode_num = programmInfo(gcode_Line)
            startingProgramm(True, prog_num)
            MC = MachineClient(gcode_num)
            gCode_Dict = MC.creating_dict_forMC()
        if type_ == 3: 
            index, cmds = preppingLine(gcode_Line)
            if index == "N1":
                print("Initialising the machine.\n")
            else:
                for cmd in cmds:
                    indexLetter = cmd[0]
                    indexNum = int(cmd[1:])
                    if indexLetter not in gCode_Dict.keys():
                        if indexLetter == 'S':
                            MC.set_spindle_speed(indexNum)
                        if indexLetter == 'F':
                            MC.set_feed_rate(indexNum)
                        if indexLetter == 'X':
                            MC.x_prime = indexNum
                        if index == 'Y':
                            MC.y_prime = indexNum
                        if indexLetter == 'Z':
                            MC.z_prime = indexNum
                    else:
                        cmd_Category = gCode_Dict[indexLetter]
                        if indexNum not in cmd_Category.keys():
                            if indexNum == 28:
                                MC.home()
                            if indexNum == 1 or indexNum == 0:
                                actionList.append(indexNum)
                if actionList[0] == 1:
                    MC.move_rapid()
                if actionList[0] == 0:
                    MC.move()
        print()
    endingProrgamm()

main()