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

    def __init__(self, numberOfGroups:int, numberOfNodes:int, groupList:list[groupStruct]=[]):
        self.groupList: list[groupStruct] = groupList
        self.numberOfGroups = numberOfGroups
        self.numberOfNodes = numberOfNodes
        self.ap=nodeStruct("00:00:00:00:00:00", 0, 0, False)
        self.gaf=dict()
        
    def createGroups(self):
        for i in range(self.numberOfGroups):
            nodeList = []
            for j in range(self.numberOfNodes):
                nodeList.append(nodeStruct("00:00:00:00:00:01", random.random(), random.random(), False))
            self.groupList.append(groupStruct(random.randint(0,len(nodeList) - 1), nodeList))

        
    def EarlyReporter(self):
        for i in range(self.numberOfGroups):
            self.groupList[i].setActiveIndex(self.groupList[i].getReporter(),True)
            self.ap.setActive(True)
            time.sleep(0.1)
            self.groupList[i].setActiveIndex(self.groupList[i].getReporter(),False)
            self.ap.setActive(False)

    def GAF(self,eventInArea: list[int]):
        for i in range(self.numberOfGroups):
            if(eventInArea[i] == True):
                self.gaf[i]=0.1
        else:
            self.gaf[-1]=1

    def withinGroupCSMA(self):
        start=time.time()
        for i in range(self.numberOfGroups):
            self.groupList[i].CSMA_CA()
        end=time.time()
        return end-start

    def process_group(self, group, time_slot_duration):
        if group in self.gaf:
            rep = self.groupList[group].getReporter()
            group_time_slot = group * time_slot_duration  
            self.groupList[group].setActiveIndex(rep, True)
            time.sleep(group_time_slot) 
            self.groupList[group].setActiveIndex(rep, False)

        time.sleep(time_slot_duration) 

    def GAP(self):
        start=time.time()
        time_slot_duration = 0.1

        processes = []
        for i in range(self.numberOfGroups):
            process = multiprocessing.Process(target=self.process_group, args=( i, time_slot_duration))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        end=time.time()
        return end-start
    
def test_gmac():
    # Initialize GMAC with 3 groups and 4 nodes per group
    gmac = GMAC(3, 4)

    # Add nodes to each group
    for i in range(gmac.numberOfGroups):
        for j in range(gmac.numberOfNodes):
            gmac.groupList[i].addNode(f"Node_{i}_{j}", random.random(), random.random(), False)

    # Test EarlyReporter
    print("Testing EarlyReporter:")
    gmac.EarlyReporter()

    # Test GAF
    print("Testing GAF:")
    event_in_area = [True, False, True]
    gmac.GAF(event_in_area)
    print(gmac.gaf)

    # Test withinGroupCSMA
    print("Testing withinGroupCSMA:")
    i=gmac.withinGroupCSMA()
    print(i)

    # Test GAP
    print("Testing GAP:")
    j=gmac.GAP()
    print(j)


if __name__ == "__main__":
    test_gmac()