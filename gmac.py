import multiprocessing
import random
import time


class nodeStruct:
    def __init__(self, mac, lat, lon, active):
        self.mac = mac
        self.lat = lat
        self.lon = lon
        self.active = active

    def getMAC(self):
        return self.mac

    def getLat(self):
        return self.lat

    def getLon(self):
        return self.lon
    
    def getActive(self):
        return self.active

    def setMAC(self, mac):
        self.mac = mac

    def setLat(self, lat):
        self.lat = lat

    def setLon(self, lon):
        self.lon = lon

    def setActive(self, active):
        self.active = active

    def __str__(self):
        return "MAC: " + self.mac + " Lat: " + str(self.lat) + " Lon: " + str(self.lon)
    

class groupStruct:
    def __init__(self, reporterIndex, nodeList ):
        self.reporter= reporterIndex
        self.nodeList = nodeList

    def addNode(self, mac, lat, lon, active):
        newNode = nodeStruct(mac, lat, lon, active)
        self.nodeList.append(newNode)

    def getReporter(self):
        return self.reporter

    def getMACIndex(self, index):
        return self.nodeList[index].getMAC()

    def getLatIndex(self, index):
        return self.nodeList[index].getLat()

    def getLonIndex(self, index):
        return self.nodeList[index].getLon()
    
    def getActivityIndex(self, index):
        return self.nodeList[index].getActive()
    
    def setReporter(self, reporterIndex):
        self.reporter = reporterIndex

    def setMAC(self, index, mac):
        self.nodeList[index].setMAC(mac)

    def setLatIndex(self, index, lat):
        self.nodeList[index].setLat(lat)

    def setLonIndex(self, index, lon):
        self.nodeList[index].setLon(lon)

    def setActiveIndex(self, index, active):
        self.nodeList[index].setActive(active)

    def __str__(self):
        return "MAC: " + self.nodeList[0].getMAC() + " Lat: " + str(self.nodeList[0].getLat()) + " Lon: " + str(self.nodeList[0].getLon()) + " Active: " + str(self.nodeList[0].getActive())

    def __len__(self):
        return len(self.nodeList)
    
    def CSMA_CA(self):
        def process_node(i):
            if not self.nodeList[i].getActive():
                is_collision = False
                for j in range(len(self.nodeList)):
                    if j != i and self.nodeList[j].getActive():
                        is_collision = True
                        break

                if is_collision:
                    backoff_time = random.uniform(0, 1) 
                    time.sleep(backoff_time)
                else:
                    self.nodeList[i].setActive(True)
                    time.sleep(0.1) 
                    self.nodeList[i].setActive(False)

        # Create a process for each node
        processes = []
        for i in range(len(self.nodeList)):
            process = multiprocessing.Process(target=process_node, args=(i,))
            processes.append(process)
            process.start()

        # Wait for all processes to finish
        for process in processes:
            process.join()



class GMAC:

    def __init__(self, numberOfGroups, numberOfNodes):
        self.groupList = []
        self.numberOfGroups = numberOfGroups
        self.numberOfNodes = numberOfNodes
        self.ap=nodeStruct("00:00:00:00:00:00", 0, 0, False)
        self.gaf=dict()
        
        for i in range(numberOfGroups):
            nodeList = []
            for j in range(numberOfGroups):
                nodeList.append(nodeStruct("00:00:00:00:00:01", random.random(), random.random(), False))
            self.groupList.append(groupStruct(i, nodeList))

        
    def EarlyReporter(self):
        for i in range(self.numberOfGroups):
            self.groupList[i].setActive(0,True)
            self.ap.setActive(True)
            time.sleep(0.1)
            self.groupList[i].setActive(0,False)
            self.ap.setActive(False)

    def GAF(self,eventInArea):
        for i in range(self.numberOfGroups):
            if(eventInArea[i] == True):
                self.gaf[i]=0.1
        else:
            self.gaf[-1]=1

if __name__ == "__main__":
    # Create a group of nodes
    group = groupStruct(0, [])

    # Add nodes to the group
    group.addNode("Node1", 10, 20, True)
    group.addNode("Node2", 15, 25, False)
    group.addNode("Node3", 30, 40, True)
    group.addNode("Node4", 35, 45, False)

    # Print the initial state of the group
    print("Initial Group State:\n")
    for i in range(len(group)):
        print(group.getMACIndex(i), group.getLatIndex(i), group.getLonIndex(i), group.getActivityIndex(i))
    print()

    # Apply CSMA/CA protocol
    start=(time.time())
    group.CSMA_CA()
    print(time.time()-start)

    # Print the final state of the group
    print("Final Group State:")
    for i in range(len(group)):
        print(group.getMACIndex(i), group.getLatIndex(i), group.getLonIndex(i), group.getActivityIndex(i))
