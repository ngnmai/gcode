'''
Assignment: G-Code interpreter 
User: Mai Nguyen 
Description: 
Implement a program that reads the attached G-Code program from a file and parses the instructions. 
The program is expected to call MachineClient's stub methods to simulate execution. 
MachineClient implements a simplified interface to control a CNC machine.
The program reads the Gcode through each line and categorize it into the code line type.
Then, the code is processed and interpreted. 
The programm is simple and is expected to be able to interprreted short gcode programm. 
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

def startingProgramm(value = "Unnamed"):
    '''
    Updating the status of the programm
    param value: str, name of the programm (if any)
    '''
    programmStatus = True
    print("Starting programm number : {}\n".format(value))

def endingProrgamm():
    '''
    Updating the status of the programm
    '''
    programmStatus = False
    print("End of programm\n")

def commenting(cmt):
    '''
    Processing the Comment in gcode
    param cmt: str, the gcode line indicates commenting
    '''
    cmt = cmt.replace('(', '')
    cmt = cmt.replace(')', '')
    print("COMMENT: " + cmt + "\n")

def programmInfo(no):
    '''
    Saving the programm's information
    param no: a string, gcode line of programme number 
    return: 1st -> number of programm (int)
            2nd -> programm numbe in gcode
    '''
    num = no.replace('o', '')
    num = num.replace('O', '')
    return int(num), no

def preppingLine(line):
    '''
    Processing the gcode line before interpretation
    param line: str, gcode line from the programm
    return: 1st -> index of the gcode line
            2nd -> a list of commands in that gcode line
    '''
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

    def set_work_offset(self):
        '''
        Setting the work offset 
        '''
        return("Moving to offset coordinates. Setting this as (0,0,0).\n")

    def set_positioning_method(self, type):
        '''
        Setting the method of positioning
        '''
        if type == 1:
            return("Setting positioning method as Increment.\n")
        else: 
            return("Setting positioning method as Absolute.\n")

    def set_prime_coordinate_x(self, xprime):
        '''
        Setting the next destination coordinates
        '''
        self.x_cor= xprime

    def set_prime_coordinate_y(self, yprime):
        '''
        Setting the next destination coordinates
        '''
        self.y_cor= yprime
    
    def set_prime_coordinate_z(self, zprime):
        '''
        Setting the next destination coordinates
        '''
        self.z_cor= zprime

    def move(self):
        '''
        Move spindle to given coordinates
        '''
        return("Moving to X={:.3f}, Y={:.3f}, Z={:.3f} [mm]\n".format(self.x_cor, self.y_cor, self.z_cor))

    def move_rapid(self):
        '''
        Move as fast as possible to a specified coordinate position
        '''
        return("Moving rapidly to X={:.3f}, Y={:.3f}, Z={:.3f} [mm]\n".format(self.x_cor, self.y_cor, self.z_cor))
    
    def set_feed_rate(self, value):
        '''
        Setting the feed rate of the spindle
        '''
        self.feed_rate = value
        return("Using feed rate {} [mm/s].\n".format(value))
    
    def set_spindle(self):
        '''
        Setting the spindle 
        '''
        return("Spindle on Clockwise\n")
    
    def stop_spindle(self):
        '''
        Stop the spindle and update status 
        '''
        self.spindle_speed = 0
        return("Spindle stop\n")

    def set_spindle_speed(self, value):
        '''
        Updating the spindle speed
        '''
        self.spindle_speed = value
        return("Using spindle speed {} [mm/s].\n".format(value))
    
    def set_tool_name(self, tool_name):
        '''
        Updating the used tool 
        '''
        self.tool = tool_name

    def change_tool(self):
        '''
        Updating the tool status
        '''
        return("Changing tool '{}'.\n".format(self.tool))
    
    def coolant_on(self):
        '''
        Updating the coolant status ON
        '''
        self.coolant_status = True
        return("Coolant turned on.\n")

    def coolant_off(self):
        '''
        Updating the cooland status OFF
        '''
        self.coolant_status = False
        return("Coolant turn off.\n")

    def creating_dict_forMC(self):
        '''
        Creating a simplified dictionary to interpret gcode to normal language
        '''
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
    #prepping the gcode before interpretation
    for gcode_Line in gcode_Lines:
        type_ = filtering(gcode_Line) #classidying the gcode line type
        actionList = []  #container for coordinates updating

        #in gcode: %
        if type_ == 0:
            pass

        #in gcode: (COMMENT)
        if type_ == 1: 
            commenting(gcode_Line)

        #in gcode: o000x - Programm number 
        if type_ == 2: 
            prog_num, gcode_num = programmInfo(gcode_Line)
            startingProgramm(prog_num) #updating the status of the programm
            MC = MachineClient(gcode_num)
            gCode_Dict = MC.creating_dict_forMC()

        #in gcode Nx - gcode 
        if type_ == 3: 
            index, cmds = preppingLine(gcode_Line)
            print(index + "\n")
            if index == "N1":
                print("Initialising the machine.\n") #ignore the initialiasing machine gcode
            else:
                for cmd in cmds: #going through each commands in a gcode line
                    indexLetter = cmd[0]
                    indexNum = float(cmd[1:])

                    #searching the command index in interpretation dictionary
                    if indexLetter not in gCode_Dict.keys():
                        if indexLetter == 'S':
                            print(MC.set_spindle_speed(indexNum))
                        if indexLetter == 'F':
                            print(MC.set_feed_rate(indexNum))
                        if indexLetter == 'X':
                            MC.set_prime_coordinate_x(indexNum)
                        if indexLetter == 'Y':
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
                #excuting the interpretation after necessary updates needed to be priotized
                if len(actionList) != 0:
                    if actionList[0] == 0:
                        print(MC.move_rapid())
                    if actionList[0] == 1:
                        print(MC.move())
    #updating the status of the programm
    endingProrgamm()

main()