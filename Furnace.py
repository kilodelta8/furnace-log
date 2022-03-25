import time
from datetime import datetime
from helpers import *


# TODO - See DOCS > Documentation > .01
class Furnace:
    '''
    class Furnace:
    none...
    Should model db model?
    '''
    furnaceNum = 0
    loadSideOrNot = False
    wagonCount = 0
    furnaceSpeed = 0
    furnaceShift = 0
    hardShiftStartAndEndTimes = []
    incomingPauseTimes = []
    totalTimeToDeduct = 0
    count = 0
    log = []
    furnaceLogActive = False



    # constructor
    def __init__(self) -> None:
        pass



    # destructor
    def __del__(self):
        self.saveLogAsFile()



    # setters
    def setFurnaceNum(self, num):
        self.furnaceNum = num


    def setLoadSideOrNot(self, side):
        self.loadSideOrNot = side


    def setWagonCount(self, count):
        self.wagonCount = count


    def setFurnaceSpeed(self, speed):
        self.furnaceSpeed = speed


    def setFurnaceShift(self, shift):
        self.furnaceShift = shift


    def setHardShiftStartAndEndTimes(self):
        if self.furnaceShift == 1:
            self.hardShiftStartAndEndTimes.append('06 45 00', '14 45 00')
        elif self.furnaceShift == 2:
            self.hardShiftStartAndEndTimes.append('14 45 00', '22 45 00')
        elif self.furnaceShift == 3:
            self.hardShiftStartAndEndTimes.append('22 45 00', '06 45 00')
        else:
            self.log.append("Failed to set shift hard start & stop times" + str(self.furnaceShift))



    # getters
    def getFurnaceNum(self):
        return self.furnaceNum


    def getLoadSideOrNot(self):
        return self.loadSideOrNot


    def getWagonCount(self):
        return self.wagonCount


    def getFurnaceSpeed(self):
        return self.furnaceSpeed


    def getFurnaceShift(self):
        return self.furnaceShift


    def getHardShiftStartTime(self):
        return self.hardShiftStartAndEndTimes[0]


    def getHardShiftEndTime(self):
        return self.hardShiftStartAndEndTimes[1]


    def getFurnaceLog(self):
        return self.log



    # mutators
    def calcTotalTimeToDeduct(self):
        '''
        calcTotalTimeToDeduct(none) -> This function is called automatically by the function "addPauseTime(time)".
        When time is added to the list, calcTotalTimeToDeduct() is called to 1. check if there are two times listed
        in the class list then 2. find the difference of the two times and store that total in the class variable.
        The function the 3. resets the list back to None.  This allows for the program to mitigate Pause times when
        they are added, providing a single amount of time to be removed from the total shift time.
        '''
        self.totalTimeToDeduct += self.incomingPauseTimes[0] - \
            self.incomingPauseTimes[1]
        self.log.append("Pause times total: " + str(round(float(self.totalTimeToDeduct) / 60.0, 3)) + " minutes.  class count > " + str(self.count))
        self.count = 0
        self.incomingPauseTimes.clear()


    def addPauseTime(self, time):
        '''
        addPauseTime(time) -> This function iterates through a class list for an open spot, as only two
        time stamps are added at maximum.  As long as the spot in the list in None (or free) the function 
        adds the time to the open spot.  The function then calls calcTotalTimeToDeduct() function to check 
        if there are two times in the list then finds the difference and adds to a class variable.
        '''
        if self.count == 0:
            self.incomingPauseTimes.append(round(time, 3))
            self.count = 1
            self.log.append(str(self.incomingPauseTimes) + " " + str(self.count))
        elif self.count == 1:
            self.incomingPauseTimes.append(round(time, 3))
            self.log.append(str(self.incomingPauseTimes) + " " + str(self.count))
            self.calcTotalTimeToDeduct()
        else:
            self.log.append("count: " + self.count +
                            " Pause times: " + str(self.incomingPauseTimes) +
                            " >>> ERROR") 


    def getTotalTimeToDeduct(self):
        '''
        getTotalTimeToDeduct(none) -> This function returns the total calculated amount of pause time that has
        been added to the class.
        '''
        return self.totalTimeToDeduct


    def getPauseCount(self):
        '''
        .
        '''
        return self.count


    def setFurnaceLogging(self, trueOrFalse):
        self.furnaceLogActive = trueOrFalse


    def writeToLog(self, data):
        if self.furnaceLogActive:
            self.log.append(str(getFormattedTimeNow()) + " >>  " + data)


    def printLog(self):
        if self.furnaceLogActive:
            for item in len(self.log):
                print(item)


    def saveLogAsFile(self):
        if self.furnaceLogActive:
            id = ("Furnace_" + str(self.furnaceNum) + "_log.txt")
            file = open(id, "a")
            tm = time.time()
            file.write("\nSaved at: " + str(time.ctime(tm)))
            file.write("Shift: " + str(self.getFurnaceShift()))
            for item in self.log:
                file.write(str(item) + "\n")
            file.write("END\n\n")
            file.close()