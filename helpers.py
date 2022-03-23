

def parseTime(timeStamp):
    '''
    Is this function even necesary???
    '''
    return timeStamp[10:19]


class PauseCalc:
    '''
    class PauseCalc:
    none...
    '''
    incomingPauseTimes = []
    totalTimeToDeduct = 0

    def __init__(self) -> None:
        pass

    def calcTotalTimeToDeduct(self):
        '''
        calcTotalTimeToDeduct(none) -> This function is called automatically by the function "addPauseTime(time)".
        When time is added to the list, calcTotalTimeToDeduct() is called to 1. check if there are two times listed
        in the class list then 2. find the difference of the two times and store that total in the class variable.
        The function the 3. resets the list back to None.  This allows for the program to mitigate Pause times when
        they are added, providing a single amount of time to be removed from the total shift time.
        '''
        if self.incomingPauseTimes.len() == 2:
            self.totalTimeToDeduct += self.incomingPauseTimes[0] - \
                self.incomingPauseTimes[1]
        for x in range(0, self.incomingPauseTimes.len()):
            self.incomingPauseTimes[x] = None

    def addPauseTime(self, time):
        '''
        addPauseTime(time) -> This function iterates through a class list for an open spot, as only two
        time stamps are added at maximum.  As long as the spot in the list in None (or free) the function 
        adds the time to the open spot.  The function then calls calcTotalTimeToDeduct() function to check 
        if there are two times in the list then finds the difference and adds to a class variable.
        '''
        for times in self.incomingPauseTimes:
            if self.incomingPauseTimes[times] is None:
                self.incomingPauseTimes[times] = time
        self.calcTotalTimeToDeduct()

    def getTotalTimeToDeduct(self):
        '''
        getTotalTimeToDeduct(none) -> This function returns the total calculated amount of pause time that has
        been added to the class.
        '''
        return self.totalTimeToDeduct
