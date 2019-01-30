# Importing re to use later for searching via regular expressions
# anytree will be used to create a tree data structure 
import re
import anytree
from anytree import Node, RenderTree

# Elevator states inputs, had to change initial formatting to import multi-line data properly using the ''' data, data ''' notation 
states = [
 # State @ t=1
 '''xx.x.x.xDxx
 xx.x.x.x.xx
 xx.x.x.x.xx
 xx.xBx.x.xx
 xx.x.xCx.xx
 xxAx.x.x.xx''',
 # State @ t=2
 '''xx.x.x.x.xx
 xx.x.x.x.xx
 xxAx.x.x.xx
 xx.xBx.x.xx
 xx.x.xCx.xx
 xx.x.x.xDxx''',
 # State @ t=3
 '''xx.x.xCx.xx
 xx.x.x.x.xx
 xx.x.x.x.xx
 xxAxBx.x.xx
 xx.x.x.x.xx
 xx.x.x.xDxx''',
 # State @ t=4
 '''xx.x.xCx.xx
 xx.x.x.x.xx
 xx.xBx.xDxx
 xx.x.x.x.xx
 xxAx.x.x.xx
 xx.x.x.x.xx''',
 # State @ t=5
 '''xx.x.xCx.xx
 xx.x.x.xDxx
 xx.x.x.x.xx
 xx.x.x.x.xx
 xxAxBx.x.xx
 xx.x.x.x.xx''',
# State @ t=6
 '''xx.x.x.x.xx
 xxAx.x.x.xx
 xx.xBx.x.xx
 xx.x.x.x.xx
 xx.x.x.x.xx
 xx.x.xCxDxx''',
 # State @ t=7
 '''xx.x.x.x.xx
 xx.x.xCx.xx
 xxAx.x.x.xx
 xx.x.x.xDxx
 xx.xBx.x.xx
 xx.x.x.x.xx'''
]

# Primary function call
def findElevatorPath(elevatorStates,startingElevator,finalDestination):
    # Trimming the data to get a simplified list format
    b = "x.\n"
    i = 0
    if (type(elevatorStates[i]) is not list):
        while i < len(elevatorStates):
            for char in b:
                elevatorStates[i] = elevatorStates[i].replace(char,"")
            elevatorStates[i] = elevatorStates[i].split(" ")
            i+=1

    # Displays the trimmed data
    # print(elevatorStates)

    # Calculates the top floor of the "building"
    def top(stateTime):
        topFloor = 0
        for str in elevatorStates[0]:
            topFloor+=1
        return topFloor

    # Takes in a state at t=n and an elevator string to find
    # the floor index of the elevator
    def floor(stateTime,elevatorStr):
        i = 0
        for str in stateTime:
            if (str.find(elevatorStr) > -1):
                return i
            i+=1

    # Instantiating initial variables for the function
    starting = startingElevator
    final = finalDestination
    finalTimeInd = int(final[2])-1
    finalFloorInd = top(elevatorStates[0]) - int(final[0])
    finalPos = (finalTimeInd,finalFloorInd)

    # Takes in a state at t=n and a floor index to find the
    # elevators currently on the floor
    def elevators(stateTime, floorIndex):
        elevators = []
        for str in stateTime[floorIndex]:
            match = re.findall(r'[A-Z]',str)
            elevators += match
        return elevators

    # Creating the initial root directory and populating it with the t = 0 values, global variable instantiation not ideal
    root = Node("root")
    def newNodes(stateTime):
        time = 0
        for str in stateTime:
            if (str != ""):
                globals()[str+time.__str__()] = Node(stateTime[floor(stateTime,str)],parent=root,pos = (time,floor(stateTime,str)))
                # This line of code instantiates new global variables in the form of "A0" (elevator+time)
                # The Node created has a parent attribute of the root directory and a position attribute
    newNodes(elevatorStates[0])

    # Populates the nodes based on the states input, once again global variables not ideal (hacker-fix)
    def addNodes(state,time,x):
        for str in state[time]:
            # If statement for floor with only one elevator
            if (str != "" and len(str) == 1):
                    globals()[str+time.__str__()] =  Node(state[time][floor(state[time],str)],parent=globals()[str+(time-1).__str__()],pos = (time,floor(state[time],str)))
            # If statement for floor with 2+ elevators
            elif (str != "" and len(str) > 1):
                    elevator = elevators(elevatorStates[time],floor(elevatorStates[time],str))
                    for i in elevator:
                            globals()[i+time.__str__()] =  Node(i,parent=globals()[str[x]+(time-1).__str__()],pos = (time,floor(state[time],i)))

    def printResult():
        # Populates the nodes into the tree data structure
        time = 1
        while (time < len(elevatorStates)):
            # If statements are due to overwrite of node variables (e.g. A2) depending on the string
            # index of the elevators on floors with 2+ elevators, probably will not scale well with additional elevator shafts
            if (starting == "B" or starting == "D"):
                addNodes(elevatorStates,time,0)
                addNodes(elevatorStates,time,1)
            elif (starting == "A" or starting == "C"):
                addNodes(elevatorStates,time,1)
                addNodes(elevatorStates,time,0)
            time+=1

        # Renders the tree for easier readability
        # print(RenderTree(root))
        result = anytree.search.findall_by_attr(root, finalPos, "pos")
        # print("result = ", result)
        if (result == ()):
            print("error: no path found")
        else:
            for i in range(len(result)):
                match = re.findall(r'/[A-Z]',result[i].__str__())
                # print("match = ", match)
            x=""
            for str in match:
                x += str[1]
            if (starting == x[0]):
                print(x)
            else:
                print("error: path not found")

    printResult()


findElevatorPath(states,"A","5-5")
findElevatorPath(states,"C","6-5")
findElevatorPath(states,"B","4-4")
findElevatorPath(states,"D","1-2")
findElevatorPath(states,"D","5-6") # Added t = 6 case to test
findElevatorPath(states,"C","3-7") # Added t = 7 case to test
