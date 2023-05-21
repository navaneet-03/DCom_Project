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
    

class GMAC:
    def __init__(self):
        self.macList = []

    def addNode(self, mac, lat, lon, active):
        newNode = nodeStruct(mac, lat, lon, active)
        self.macList.append(newNode)

    def getMAC(self, index):
        return self.macList[index].getMAC()

    def getLat(self, index):
        return self.macList[index].getLat()

    def getLon(self, index):
        return self.macList[index].getLon()
    
    def getActive(self, index):
        return self.macList[index].active()

    def setMAC(self, index, mac):
        self.macList[index].setMAC(mac)

    def setLat(self, index, lat):
        self.macList[index].setLat(lat)

    def setLon(self, index, lon):
        self.macList[index].setLon(lon)

    def setActive(self, index, active):
        self.macList[index].setActive(active)

    def __str__(self):
        return "MAC: " + self.macList[0].getMAC() + " Lat: " + str(self.macList[0].getLat()) + " Lon: " + str(self.macList[0].getLon())

    def __len__(self):
        return len(self.macList)

    