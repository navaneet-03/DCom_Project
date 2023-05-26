import multiprocessing
import random
import time


class nodeStruct:
    def __init__(self, mac: str, lat: float, lon: float, active: bool):
        self.mac = mac
        self.lat = lat
        self.lon = lon
        self.active = active

    def getMAC(self)->str:
        return self.mac

    def getLat(self)->float:
        return self.lat

    def getLon(self)->float:
        return self.lon
    
    def getActive(self)->bool:
        return self.active

    def setMAC(self, mac)->None:
        self.mac = mac

    def setLat(self, lat)->None:
        self.lat = lat

    def setLon(self, lon)->None:
        self.lon = lon

    def setActive(self, active)->None:
        self.active = active

    def __str__(self)->str:
        return "MAC: " + self.mac + " Lat: " + str(self.lat) + " Lon: " + str(self.lon)
    

class groupStruct:
    def __init__(self, reporterIndex: int, nodeList : list[nodeStruct]):
        self.reporter= reporterIndex
        self.nodeList = nodeList

    def addNode(self, mac: str, lat: float, lon: float, active:bool)->None:
        newNode = nodeStruct(mac, lat, lon, active)
        self.nodeList.append(newNode)

    def getReporter(self)->int:
        return self.reporter

    def getMACIndex(self, index:int)->str:
        return self.nodeList[index].getMAC()

    def getLatIndex(self, index:int)->float:
        return self.nodeList[index].getLat()

    def getLonIndex(self, index:int) ->float:
        return self.nodeList[index].getLon()
    
    def getActivityIndex(self, index:int)->bool:
        return self.nodeList[index].getActive()
    
    def setReporter(self, reporterIndex:int)->None:
        self.reporter = reporterIndex

    def setMAC(self, index:int, mac:str)->None:
        self.nodeList[index].setMAC(mac)

    def setLatIndex(self, index:int, lat:float)->None:
        self.nodeList[index].setLat(lat)

    def setLonIndex(self, index:int, lon:float)->None:
        self.nodeList[index].setLon(lon)

    def setActiveIndex(self, index:int, active:bool)->None:
        self.nodeList[index].setActive(active)

    def __str__(self)->str:
        return "MAC: " + self.nodeList[0].getMAC() + " Lat: " + str(self.nodeList[0].getLat()) + " Lon: " + str(self.nodeList[0].getLon()) + " Active: " + str(self.nodeList[0].getActive())

    def __len__(self)->int:
        return len(self.nodeList)
    
    def CSMA_CA(self)->float:
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

    def __init__(self, numberOfGroups:int, numberOfNodes:int):
        self.groupList: list[groupStruct] = []
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
            self.groupList[self.groupList.reporter].setActive(0,True)
            self.ap.setActive(True)
            time.sleep(0.1)
            self.groupList[self.groupList.reporter].setActive(0,False)
            self.ap.setActive(False)

    def GAF(self,eventInArea: list[int]):
        for i in range(self.numberOfGroups):
            if(eventInArea[i] == True):
                self.gaf[i]=0.1
        else:
            self.gaf[-1]=1

    def withinGroupCSMA(self):
        for i in range(self.numberOfGroups):
            self.groupList[i].CSMA_CA()

    def process_group(self, group, time_slot_duration):
        if group in self.gaf:
            rep = self.groupList[group].getReporter()
            group_time_slot = group * time_slot_duration  
            self.groupList[rep].setActive(rep, True)
            time.sleep(group_time_slot) 
            self.groupList[rep].setActive(rep, False)

        time.sleep(time_slot_duration) 

    def GAP(self):
        time_slot_duration = 0.1

        processes = []
        for i in range(self.numberOfGroups):
            process = multiprocessing.Process(target=self.process_group, args=(self, i, time_slot_duration))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()
    

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

    print()
    # Create an instance of GMAC
    gmac = GMAC(numberOfGroups=2, numberOfNodes=3)

    # Set the initial state of the nodes
    gmac.groupList[0].setActiveIndex(0, True)
    gmac.groupList[1].setActiveIndex(0, True)
    gmac.groupList[1].setActiveIndex(1, True)

    # Invoke the CSMA_CA method to simulate the protocol
    gmac.groupList[0].CSMA_CA()
    gmac.groupList[1].CSMA_CA()

    # Print the state of the nodes after the CSMA-CA protocol
    for i in range(len(gmac.groupList)):
        print("Group", i)
        for j in range(len(gmac.groupList[i])):
            print("Node", j)
            print("MAC:", gmac.groupList[i].getMACIndex(j))
            print("Lat:", gmac.groupList[i].getLatIndex(j))
            print("Lon:", gmac.groupList[i].getLonIndex(j))
            print("Active:", gmac.groupList[i].getActivityIndex(j))
            print()

