import multiprocessing
import random
import time
import gmac

class Sub_GMAC:
    def __init__(self,numberOfGroups, numberOfNodes) -> None:
        self.groupList: list[gmac.groupStruct] = []
        self.numberOfGroups = numberOfGroups
        self.numberOfNodes = numberOfNodes
        self.ap=gmac.nodeStruct("00:00:00:00:00:00", 0, 0, False)
        #self.gaf=dict()
        self.subGroupList: list[gmac.GMAC]=[]
        
    def createGroups(self):
        for i in range(self.numberOfGroups):
            nodeList = []
            for j in range(self.numberOfNodes):
                nodeList.append(gmac.nodeStruct("00:00:00:00:00:01", random.random(), random.random(), False))
            self.groupList.append(gmac.groupStruct(random.randint(0,len(nodeList) - 1), nodeList))
    
    def EarlyReporter(self):
        for i in range(self.numberOfGroups):
            self.groupList[i].setActiveIndex(self.groupList[i].getReporter(),True)
            self.ap.setActive(True)
            time.sleep(0.1)
            self.groupList[i].setActiveIndex(self.groupList[i].getReporter(),False)
            self.ap.setActive(False)

    def subGMACCreation(self,grouping:int):
        i=0
        while i * grouping < self.numberOfGroups:
            self.subGroupList.append(gmac.GMAC(grouping,self.numberOfNodes,self.groupList[i * grouping:(i + 1) * grouping]))
            i+=1
        else:
            self.subGroupList.append(gmac.GMAC(self.numberOfGroups - i * grouping,self.numberOfNodes,self.groupList[i * grouping:self.numberOfGroups]))

    def run(self,eventInArea):
        self.createGroups()
        self.subGMACCreation(2)
        for i in range(len(self.subGroupList)):
            self.gaf[i]=multiprocessing.Process(target=self.subGroupList[i].sub_run, args=(eventInArea[i],))
            self.gaf[i].start()
        self.EarlyReporter()
        for i in range(len(self.subGroupList)):
            self.gaf[i].join()
        print("Done")