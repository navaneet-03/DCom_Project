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
    def __init__(self, reporterIndex, macList ):
        self.reporter= reporterIndex
        self.macList = macList

    def addNode(self, mac, lat, lon, active):
        newNode = nodeStruct(mac, lat, lon, active)
        self.macList.append(newNode)

    def getReporter(self):
        return self.reporter

    def getMAC(self, index):
        return self.macList[index].getMAC()

    def getLat(self, index):
        return self.macList[index].getLat()

    def getLon(self, index):
        return self.macList[index].getLon()
    
    def getActive(self, index):
        return self.macList[index].active()
    
    def setReporter(self, reporterIndex):
        self.reporter = reporterIndex

    def setMAC(self, index, mac):
        self.macList[index].setMAC(mac)

    def setLat(self, index, lat):
        self.macList[index].setLat(lat)

    def setLon(self, index, lon):
        self.macList[index].setLon(lon)

    def setActive(self, index, active):
        self.macList[index].setActive(active)

    def __str__(self):
        return "MAC: " + self.macList[0].getMAC() + " Lat: " + str(self.macList[0].getLat()) + " Lon: " + str(self.macList[0].getLon()) + " Active: " + str(self.macList[0].getActive())

    def __len__(self):
        return len(self.macList)
    
    def CSMA_CA(self):
        for i in range(len(self.macList)):
            if(self.macList[i].getActive() == False):
                for j in range(len(self.macList)):
                    if(self.macList[j].getActive() == True):
                        self.setActive(j,True)
                        self.setActive(i,True)
                        time.sleep(0.1)
                        self.setActive(j,False)
                        self.setActive(i,False)
                        break



class GMAC:

    def __init__(self, numberOfGroups, numberOfNodes):
        self.groupList = []
        self.numberOfGroups = numberOfGroups
        self.numberOfNodes = numberOfNodes

        ap=nodeStruct("00:00:00:00:00:00", 0, 0, False)
        for i in range(numberOfGroups):
            nodeList = []
            for j in range(numberOfGroups):
                nodeList.append(nodeStruct("00:00:00:00:00:01", random.random(), random.random(), False))
            self.groupList.append(groupStruct(i, nodeList))

        
        

