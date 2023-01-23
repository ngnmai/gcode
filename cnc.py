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
    print(str("COMMENT: " + cmt + "\n")) 

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
    index = cmd_s[0]
    commands = cmd_s[1:]
    return index, commands


class MachineClient:
    def __init__(self,name):
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
        return("Moving to home.\n")

    def set_work_offset(self, flag = True):
        if flag == True:
            return("Moving to offset coordinates. Setting this as (0,0,0).\n")

    def set_positioning_method(self, type, flag = True):
        if flag == True:
            if type == 1:
                return("Setting positioning method as Increment.\n")
            else: 
                return("Setting positioning method as Absolute.\n")

    def set_prime_coordinate_x(self, xprime):
        '''
        Setting the next destination coordinates
        '''
        self.x_prime= xprime
        self.y_prime = self.y_cor
        self.z_prime = self.z_cor

    
    def set_prime_coordinate_y(self, yprime):
        '''
        Setting the next destination coordinates
        '''
        self.y_prime= yprime
        self.x_prime = self.x_cor
        self.z_prime = self.z_cor

    
    def set_prime_coordinate_z(self, zprime):
        '''
        Setting the next destination coordinates
        '''
        self.z_prime= zprime
        self.x_prime = self.x_cor
        self.y_prime = self.y_cor


    def move(self):
        '''
        Move spindle to given coordinates
        '''
        self.x_cor, self.y_cor, self.z_cor = self.x_prime, self.y_prime, self.z_prime
        return("Moving to X={:.3f}, Y={:.3f}, Z={:.3f} [mm]\n".format(self.x_cor, self.y_cor, self.z_cor))

    def move_rapid(self):
        '''
        Move as fast as possible to a specified coordinate position
        '''
        self.x_cor, self.y_cor, self.z_cor = self.x_prime, self.y_prime, self.z_prime
        return("Moving rapidly to X={:.3f}, Y={:.3f}, Z={:.3f} [mm]\n".format(self.x_cor, self.y_cor, self.z_cor))
    
    def set_feed_rate(self, value):
        self.feed_rate = value
        return("Using feed rate {} [mm/s].\n".format(value))
    
    def set_spindle(self, flag = True):
        if flag == True:
            return("Spindle on Clockwise\n")
    
    def stop_spindle(self, flag = True):
        if flag == True:
            self.spindle_speed = 0
            return("Spindle stop\n")

    def set_spindle_speed(self, value):
        self.spindle_speed = value
        return("Using spindle speed {} [mm/s].\n".format(value))
    
    def set_tool_name(self, tool_name, flag = True):
        if flag == True:
            self.tool = tool_name

    def change_tool(self, flag = True):
        if flag == True:
            return("Changing tool '{}'.\n".format(self.tool))
    
    def coolant_on(self):
        self.coolant_status = True
        return("Coolant turned on.\n")

    def coolant_off(self, flag = True):
        if flag == True:
            self.coolant_status = False
            return("Coolant turn off.\n")

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
        actionList = []
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
            print(index + "\n")
            if index == "N1":
                print("Initialising the machine.\n")
            else:
                for cmd in cmds:
                    indexLetter = cmd[0]
                    indexNum = float(cmd[1:])
                    if indexLetter not in gCode_Dict.keys():
                        if indexLetter == 'S':
                            print(MC.set_spindle_speed(indexNum))
                        if indexLetter == 'F':
                            print(MC.set_feed_rate(indexNum))
                        if indexLetter == 'X':
                            MC.set_prime_coordinate_x(indexNum)
                        if index == 'Y':
                            MC.set_prime_coordinate_y(indexNum)
                        if indexLetter == 'Z':
                            MC.set_prime_coordinate_z(indexNum)
                    else:
                        cmd_Category = gCode_Dict[indexLetter]
                        if int(indexNum) not in cmd_Category.keys():
                            if indexNum == 28:
                               print(MC.home())
                            if indexNum == 1 or indexNum == 0:
                                actionList.append(indexNum)
                        else:
                            output = cmd_Category[indexNum]
                            if output != None:
                                print(output)
                if len(actionList) != 0:
                    if actionList[0] == 1:
                        print(MC.move_rapid())
                    if actionList[0] == 0:
                        print(MC.move())
        print()
    endingProrgamm()

main()