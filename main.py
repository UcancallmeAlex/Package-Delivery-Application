
import csv
from collections import defaultdict


#Learned how to create a hashmap from youtube video https://www.youtube.com/watch?v=9HFbhPscPU0 by Joe James
#Used largely similar code as there are few ways of varying the implementation.
class HashMap:
    #Constructor for HashMap, size is set to 64 but can be adjusted, creates empty list of size 64
    def __init__(self):
        self.size = 64
        self.map = [None] * self.size
    #Function that hashes the key for the hashmap. Adds up the values of the chars in the string and modulos it by the size of the hashmap
    def _getHash(self, key):
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size
    #Function for adding a key value pair to the hashmap, calls _getHash(key) to hash the key
    def add(self, key, value):
        keyHash = self._getHash(key)
        keyValue = [key, value]
        #If statement that checks if the key is already found, if its found it either replaces the new value if its the same key,
        #or chains a new pair to the collided hash
        if self.map[keyHash] is None:
            self.map[keyHash] = list([keyValue])
            return True
        else:
            for pair in self.map[keyHash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[keyHash].append(keyValue)
            return True
    #Function that returns the value associated with the key
    def get(self, key):
        keyHash = self._getHash(key)
        if self.map[keyHash] is not None:
            for pair in self.map[keyHash]:
                if pair[0] == key:
                    return pair[1]
        return None
    #Function that deletes the key value pair for a given key from the hashmap
    def delete(self, key):
        keyHash = self._getHash(key)
        if self.map[keyHash] is None:
            return False
        for i in range (0, len(self.map[keyHash])):
            if self.map[keyHash][i][0] == key:
                self.map[keyHash].pop(i)
                return True
    #Function that prints each object stored in the map
    def print(self):
        print("Package hashmap:")
        for item in self.map:
            if item is not None:
                print(str(item))
    #Function I created specifically for this program, to iterate through the hashmap and return a list of all objects
    #in the hashmap
    def iterate(self):
        listAll = []
        for i in range (1, self.size):
            if self.get(str(i)) is not None:
                listAll.append(self.get(str(i)))
        return listAll

    #lookUp function takes in a package id, and returns the various data components of the package, as well as printing
    #each component in a readable manner.
    def lookUp(self, id):
        packageInspected = self.get(str(id))
        lookupAddress = packageInspected.address
        lookupDeadline = packageInspected.deadline
        lookupCity = packageInspected.city
        lookupZip = packageInspected.zipcode
        lookupWeight = packageInspected.kilo
        lookupStatus = packageInspected.status
        lookupTime = packageInspected.timeDelivered
        #If statement checks the type of the timeDelivered component of the package object.
        #The objects timeDelivered is initialized as a string: "Not Delivered" so only performs the following statements
        #if the package has been delivered and the timeDelivered is a float
        #The code then converts the time that would be passed in as a float of minutes past 8:00 am, into a readable time format
        #example 30 minutes passed in would covert to 8:30
        if type(lookupTime) != str:
            timeDiv = int(lookupTime) // 60
            timeDiv += 8
            timeRem = int(lookupTime) % 60
            if timeRem < 10:
                timeRem = "0" + str(timeRem)
            timeDiv = str(timeDiv)
            timeRem = str(timeRem)
            lookupTime = timeDiv + ":" + timeRem

        #Print statements display package data
        print("Package " + str(id) + ": " + str(lookupAddress) + " " + str(lookupCity) + ", " + str(lookupZip) + ". Weight: " + str(lookupWeight) + " kilos.")
        print("Deadline: " + str(lookupDeadline) + ". Status: " + str(lookupStatus) + ". Time delivered: " + lookupTime + ".")

        return lookupAddress, lookupDeadline, lookupCity, lookupZip, lookupWeight, lookupStatus, lookupTime

    #copyMap function which is used in the truck's snapshot function to create a copy of the package hashmap to provide a
    #snapshot of package delivery states and their times. Also calls the copyPackage function to create copies of the package
    #objects which are then stored in the new hashmap copy.
    #Returns the new copy of the hashmap
    def copyMap(self):
        newList = self.iterate()
        newMap = HashMap()
        for each in newList:
            packageCopy = each.copyPackage(each.status, each.timeDelivered)
            newMap.add(packageCopy.id, packageCopy)

        return newMap

#Truck class
class Truck:
    #Constructor that creates truck objects, each truck has its own cargo hashmap as well as a deliveryList, a dictionary that is used
    #in the nearestDelivery algorithm. The starting time 0 is used for 8:00 am. In the main function Truck 2's starting time is set
    #for 10:30
    def __init__(self, truckName):
        self.name = truckName
        self.cargo = HashMap()
        self.deliveryList = {}
        self.miles = 0
        self.location = "HUB"
        self.startingTime = 0

    #addPackage function is used manually in the main function. Each package added will add to the truck's cargo hashmap
    #and also updates the deliveryList dictionary with the destination for delivery, with a value of 1 just as a placeholder.
    #The package's status is then updated to being "En route in " whichever truck it is added to.
    #If a package with the same delivery address is added, the deliveryList will just overwrite that item to prevent duplicates.
    def addPackage(self, package):
        package.status = ("En route in " + self.name)
        self.cargo.add(package.id, package)
        self.deliveryList[package.address] = 1

    #This is essentially the Nearest Neighbor algorithm implemented for this specific project. It takes in the truck's current
    #location, and ends up returning the nearest ending delivery destination.
    def nearestDelivery(self, currentLocation):
        #Initializing comparison variables. shortestEdgeMiles is set arbitrarily to 100.0 in order to compare available edge
        #distances and find the smallest.
        endingVertex = None
        shortestEdgeMiles = 100.0

    #This loop is going through the edges[currentLocation] list and checking if it can be found in the trucks
    #current deliveryList. If it finds one then it will compare to find the shortest edge
        for i in range(len(edges[currentLocation])):
            #print(edges[currentLocation][i].vertexTwo)
            #print statement for debugging

            if edges[currentLocation][i].vertexTwo in self.deliveryList:
                #print("found in list" + edges[currentLocation][i].vertexTwo)
                #print statement for debugging
                if edges[currentLocation][i].miles < shortestEdgeMiles:
                    shortestEdgeMiles = edges[currentLocation][i].miles
                    endingVertex = edges[currentLocation][i].vertexTwo

        #After finding the nearest delivery, the truck adds the edge distance to its total miles and adjusts its location
        #to the new location, the ending vertex of the shortest edge.
        self.miles += shortestEdgeMiles
        self.location = endingVertex
        #After assigning new location of the truck, the current location in the deliveryList dictionary is popped as the truck
        #no longer needs to return for the current deliveries
        self.deliveryList.pop(self.location)
        #Calls the deliverPackage function that handles package delivery logic.
        self.deliverPackage()

        return endingVertex

    #deliverPackage function iterates through the cargo hashmap on the truck, which returns a list of the package objects.
    #Then it calculates the time of the delivery by determining the miles traveled and the speed of the truck, as well as the
    #starting time. If the currentPackages list is not empty. The function will loop through this list of packages and find
    #any that have a destination that is the same as the current location of the truck. Those packages will then have
    #their delivery status set to "Delivered", the timeDelivered is set to the current minutes past 8:00 am, and then
    #the package is removed from the cargo. Every time packages are delivered, the snapshot function is called.
    def deliverPackage(self):
        currentPackages = self.cargo.iterate()
        minutes = (self.miles / 18.0) * 60
        minutes = int(minutes)
        minutes += self.startingTime

        if len(currentPackages) > 0:
            for each in currentPackages:
                if each.address == self.location:
                    packageDelivered = packageHashMap.get(each.id)
                    packageDelivered.status = "Delivered"
                    print("Package: " + each.id + " delivered.")
                    packageDelivered.timeDelivered = minutes
                    self.cargo.delete(each.id)

            self.snapshot()

    #The snapshot function is used to keep track of when packages are delivered and provide a list of all packages and their
    #status at any given moment.
    def snapshot(self):

        #Creates a copy of the current packageHashMap, which contains all of the package objects and their current status at the given time.
        snapshotMap = packageHashMap.copyMap()
        minutes = (self.miles / 18.0) * 60
        minutes = int(minutes)
        minutes += self.startingTime
        #This is a bit of inelegant code used simply to prevent certain collisions.
        if minutes in snapshotList:
            minutes += 1

        #Adds the current snapshot time in minutes to the snapshotList, which is essentially a list of keys for the snapshotDict
        snapshotList.append(minutes)
        #Adds the copy of the package hashmap to a dictionary of hashmaps, with the key being the string type cast of the
        #time in minutes
        snapshotDict[str(minutes)] = snapshotMap

#Package class
class Package:
    #Package constructor that initializes each package's data components.
    def __init__(self, packageID, address, city, state, zipCode, deadline, kilo, notes):
        self.id = packageID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipCode
        self.deadline = deadline
        self.kilo = kilo
        self.notes = notes
        self.status = "at the hub"
        self.timeDelivered = "Not yet delivered"

    #printPackage function used for debugging.
    def printPackage(self):
        print("package id: " + self.id + " " + self.address + " " + self.notes)

    #copyPackage function is used to create a copy of each package object and their current status at a given time. This is used
    #in the copyMap and snapshot functions. Returns the new copy of the package
    def copyPackage(self, statusCopy, timeDeliveredCopy):
        newPackage = Package(self.id, self.address, self.city, self.state, self.zipcode, self.deadline, self.kilo, self.notes)
        newPackage.status = statusCopy
        newPackage.timeDelivered = timeDeliveredCopy
        return newPackage

#Loads package data from csv file, creating a package object for each line in csv, and storing it in a packageDataList.
#The package data list is returned from the function and then added to the packageHashMap in the main function.
#This existence of packageDataList is perhaps redundant but is left for what I believe is simpler readability.
def loadPackageData(filename):
    with open(filename) as packageDataFile:
        packageData = csv.reader(packageDataFile, delimiter=',')
        #Skips header line
        next(packageData)
        packageDataList = []
        for package in packageData:
            pID = package[0]
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeadline = package[5]
            pKilo = package[6]
            pNotes = package[7]

            p = Package(pID, pAddress, pCity, pState, pZip, pDeadline, pKilo, pNotes)
            packageDataList.append(p)
        return packageDataList

#Loads distance data from csv file, creating a vertex object for each address, and two edge objects to and from each vertex.
def loadDistanceData(filename):
    with open(filename) as distanceDataFile:
        #Creates an empty list of vertices and a defaultdict of lists of edges. Honestly I forgot why I used a defaultdict instead
        #of a normal dictionary, but it fixed a bug I was encountering.
        vertices = []
        edges = defaultdict(list)

        distanceData = csv.reader(distanceDataFile, delimiter=',')
        #Skips header line
        next(distanceData)
        counterIndex = int(0)
        addressList = []
        #Each address parsed from the csv file is added to the addressList list.
        for address in distanceData:
            addressList.append(address[0])
            v = Vertex(addressList[counterIndex])
            vertices.append(v)
            #After each line in the csv, a new vertex is added, this nested loop attaches edges of the new vertex to previous vertices.
            #Because each vertex added, adds a new possible edge to each vertex prior, two indexs are used, i and the counterIndex.
            #as the counterIndex increases, which increases by one for every edge, i is then set to that index and decremented until the
            #loop passes for each previous vertex. Two Edge objects are created on each pass, one forward and one in reverse, and the distance
            #is added for the m field. Example A->B with miles of x and B->A with miles of x.
            if counterIndex > 0:
                i = counterIndex
                while i > 0:
                    i -= 1
                    eOne = Edge(addressList[counterIndex], addressList[i], float(address[i + 1]))
                    eTwo = Edge(addressList[i], addressList[counterIndex], float(address[i + 1]))
                    edges[eOne.vertexOne].append(eOne)
                    edges[eTwo.vertexOne].append(eTwo)

            counterIndex += 1
        return vertices, edges


#Vertex and edge classes
class Vertex:
    def __init__(self, n):
        self.name = n
class Edge:
    #Constructor for Edge object. Creates an edge with a starting and ending vertex, and the miles between them.
    def __init__(self, vOne, vTwo, m):
        self.vertexOne = vOne
        self.vertexTwo = vTwo
        self.miles = m
        #print("Making edge from " + self.vertexOne + " to " + self.vertexTwo + " with a weight of " + self.miles + " miles.")
        #used for debugging

#Global variables
#Hashmap that stores package objects
packageHashMap = HashMap()
#List of vertices
vertices = []
#Dictionary of edges
edges = {}
#List of snapshot times
snapshotList = []
#Dictionary of snapshot hashmaps with time values in snapshotList used as keys.
snapshotDict = {}


#Global functions

#roundDown function was created to convert any valid user entered time input into the appropriate snapshot time value
#associated with the snapshotList
def roundDown(timeInput):
    #Comparison variable initialized to arbitrary value
    minDiff = 1600
    #Subtracting 8 hours from the input, as the time values used in other functions are passed as minutes past 8:00 am.
    convertedInput = timeInput - 8
    convertedInput *= 60
    convertedInput = int(convertedInput)

    #If the convertedInput is negative, that means the user entered an input earlier than 8:00 am so it will return 0 for the
    #default snapshot time value.
    if convertedInput < snapshotList[0]:
        return 0

    #This loop then goes through each value in the snapshotList (whose length increases by 1 for every snapshot) to find
    #the closest value in the list before the inputted time, or the exact time of a snapshot if the user happened to enter an
    #exact time. The time then subtracts the difference from the closest time previous and returns that convertedInput which
    #should now be a time value on the snapshotList.
    for each in snapshotList:
        if convertedInput - each < 0:
            convertedInput -= minDiff
            return convertedInput
        elif convertedInput - each == 0:
            return convertedInput
        elif convertedInput - each < minDiff:
            minDiff = convertedInput - each

    convertedInput -= minDiff
    return convertedInput

#Function that takes a given time and provides the status of all packages in the hashmap at that given snapshot time.
#iterates through every package id number and calls the lookup function for the specific hashmap that is stored in the
#snapshotDict dictionary. Reminder the snapshotDict is a dictionary whose keys are specific time values, and whose values
#are specific hashmaps, copied from the packageHashMap at a specific time.
def snapshotAll(time):
    for i in range(1,41):
        snapshotDict[str(time)].lookUp(str(i))

#The compileSnapshot function is called near the end of the main function. Its purpose is to update, in order, the copied
#hashmaps of packages, that are stored in the snapshotDict. If the compileSnapshot function were NOT called, the snapshotted
#hashmaps would each only have the packages delivery status correct on only one snapshotted hashmap, the snapshot during which
#those packages were delivered. Example packages delivered at 9:00 would be marked as delivered at 9:00 and then in the next delivery
#at say 9:30, would be reset and marked undelivered in the next snapshotted hashmap at 9:30 in which different packages were delivered.
#Debugging this and working out the compileSnapshot function was probably the most challenging part of the project for me, and most
#likely is a naive solution, that is far from optimal.
def compileSnapshot():
    #Will start by iterating through the snapshotDict and creating copies of the previous snapshot map at the time
    #that is found by using the values of snapshotList items, which are specific times, and then using those as the key
    #in the snapshotDict. Then creates a list of the packages in the current snapshot map for comparison.
    #The nested loop then goes through that list of packages and inelegantly checks the delivery status of the package.
    #If it finds the status different from the default, which is "Not yet delivered", it will change the copy of the hashmap
    #to the correct status at that time, and then replace the snapshot hashmap in the snapshotDict with that updated copy.
    #This process repeats for each snapshot in the snapshotDict, essentially merging each hashmap with the previous hashmap
    #to undo the overwritten values.
    for i in range(1, len(snapshotList)):
        newCopy = snapshotDict[str(snapshotList[i-1])].copyMap()
        newList = snapshotDict[str(snapshotList[i])].iterate()
        for j in range(len(newList)):
            if newList[j].status == "Delivered":
                newCopy.get(newList[j].id).status = newList[j].status
                newCopy.get(newList[j].id).timeDelivered = newList[j].timeDelivered
            elif newList[j].status == "En route in Truck 1":
                newCopy.get(newList[j].id).status = newList[j].status
            elif newList[j].status == "En route in Truck 2":
                newCopy.get(newList[j].id).status = newList[j].status
            if j == 8:
                if newList[j].address == "410 S State St":
                    newCopy.get(newList[j].id).address = newList[j].address
                    newCopy.get(newList[j].id).zipcode = newList[j].zipcode

        snapshotDict[str(snapshotList[i])] = newCopy


if __name__ == '__main__':

    #Loading package data from "Package File.csv"
    packageDataList = loadPackageData("Package File.csv")

    #Adding data from "Package File.csv" into a HashMap object
    for each in packageDataList:
        packageHashMap.add(each.id, each)

    #Loading distance data from Distance Table.csv
    vertices, edges = loadDistanceData("Distance Table.csv")

    #Intializing truck objects
    truckOne = Truck("Truck 1")
    truckTwo = Truck("Truck 2")

    #Initializing snapshot list and dictionary at start of day (8:00 am)
    snapshotDict["0"] = packageHashMap.copyMap()
    snapshotList.append(0)

    #Setting Truck starting locations
    truckOne.location = "HUB"
    truckTwo.location = "HUB"

    #Loading Truck One with first load for items with early deadlines
    truckOne.addPackage(packageHashMap.get("1"))
    truckOne.addPackage(packageHashMap.get("7"))
    truckOne.addPackage(packageHashMap.get("13"))
    truckOne.addPackage(packageHashMap.get("14"))
    truckOne.addPackage(packageHashMap.get("15"))
    truckOne.addPackage(packageHashMap.get("16"))
    truckOne.addPackage(packageHashMap.get("19"))
    truckOne.addPackage(packageHashMap.get("20"))
    truckOne.addPackage(packageHashMap.get("21"))
    truckOne.addPackage(packageHashMap.get("29"))
    truckOne.addPackage(packageHashMap.get("30"))
    truckOne.addPackage(packageHashMap.get("31"))
    truckOne.addPackage(packageHashMap.get("34"))
    truckOne.addPackage(packageHashMap.get("37"))
    truckOne.addPackage(packageHashMap.get("39"))
    truckOne.addPackage(packageHashMap.get("40"))



    #First delivery trip for truck one
    #Calls nearestDelivery function as long as the truck has a delivery list
    while len(truckOne.deliveryList) > 0:
        truckOne.nearestDelivery(truckOne.location)

    #Returning Truck One to the hub
    #Creates an entry in the deliveryList dict and uses the nearestDelivery to return the truck to the hub
    truckOne.deliveryList["HUB"] = 1
    truckOne.nearestDelivery(truckOne.location)
    print("Returning truck 1 to hub...")

    #Second Load for Truck One, packages with deadline of 10:30
    truckOne.addPackage(packageHashMap.get("6"))
    truckOne.addPackage(packageHashMap.get("25"))
    truckOne.addPackage(packageHashMap.get("26"))

    #Second delivery trip for truck one
    while len(truckOne.deliveryList) > 0:
        truckOne.nearestDelivery(truckOne.location)

    #Updating package #9 at 10:20 am
    packageNine = packageHashMap.get("9")
    packageNine.address = "410 S State St"
    packageNine.zipcode = "84111"

    #Setting Truck Two delivery start time to 10:30 am (adds time in minutes to 8:00 am in the truck delivery function)
    truckTwo.startingTime = 150

    #Loading Truck Two
    truckTwo.addPackage(packageHashMap.get("2"))
    truckTwo.addPackage(packageHashMap.get("3"))
    truckTwo.addPackage(packageHashMap.get("4"))
    truckTwo.addPackage(packageHashMap.get("5"))
    truckTwo.addPackage(packageHashMap.get("8"))
    truckTwo.addPackage(packageHashMap.get("9"))
    truckTwo.addPackage(packageHashMap.get("10"))
    truckTwo.addPackage(packageHashMap.get("11"))
    truckTwo.addPackage(packageHashMap.get("12"))
    truckTwo.addPackage(packageHashMap.get("17"))
    truckTwo.addPackage(packageHashMap.get("18"))
    truckTwo.addPackage(packageHashMap.get("22"))
    truckTwo.addPackage(packageHashMap.get("23"))
    truckTwo.addPackage(packageHashMap.get("24"))
    truckTwo.addPackage(packageHashMap.get("27"))
    truckTwo.addPackage(packageHashMap.get("28"))


    #First delivery trip for truck two
    # Calls nearestDelivery function as long as the truck has a delivery list
    while len(truckTwo.deliveryList) > 0:
        truckTwo.nearestDelivery(truckTwo.location)


    #Returning Truck Two to the hub
    #Creates an entry in the deliveryList dict and uses the nearestDelivery to return the truck to the hub
    truckTwo.deliveryList["HUB"] = 1
    truckTwo.nearestDelivery(truckTwo.location)
    print("Returning truck 2 to hub...")



    #Second Load for Truck Two
    truckTwo.addPackage(packageHashMap.get("32"))
    truckTwo.addPackage(packageHashMap.get("33"))
    truckTwo.addPackage(packageHashMap.get("35"))
    truckTwo.addPackage(packageHashMap.get("36"))
    truckTwo.addPackage(packageHashMap.get("38"))



    #Second delivery trip for truck two
    while len(truckTwo.deliveryList) > 0:
            truckTwo.nearestDelivery(truckTwo.location)

    #Sorting list of snapshots, used to compare time input and round down to nearest snapshot in list
    snapshotList = sorted(snapshotList)


    #Adding total miles
    totalMiles = truckOne.miles + truckTwo.miles
    truckOne.miles = round(truckOne.miles, 2)
    truckTwo.miles = round(truckTwo.miles, 2)
    totalMiles = round(totalMiles, 2)
    print("Truck 1 miles: " + str(truckOne.miles))
    print("Truck 2 miles: " + str(truckTwo.miles))
    print("Total miles: " + str(totalMiles))

    packageHashMap.lookUp("9")

    #Compiles the snapshots together
    compileSnapshot()

    #Input UI loop
    #If user something invalid the program WILL likely crash.
    #Please enter either 'all' or a valid package id for the first option, and a proper time in the format 0.00 to 24.00
    #for the second prompt
    userInput = "NULL"
    while userInput.lower() != "quit":
        userInput = input("Options:\nEnter 'all' for status of all packages\nEnter ID# for one package 1 to 40 ex: '5'\n")
        if userInput == "all":
            userInput = input("Enter a time in the format 0.00 to 24.00\nExample: 13.15 for 1:15 PM\n")
            snapshotAll(str(roundDown(float(userInput))))
        else:
            numInput = userInput
            userInput = input("Enter a time in the format 0.00 to 24.00\nExample: 13.15 for 1:15 PM\n")
            snapshotDict[str(roundDown(float(userInput)))].lookUp(str(numInput))


