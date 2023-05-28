import matplotlib.pyplot as plt
import numpy as np
import gmac
import sub_gmac

def main():
    numberOfNodes = 5
    timeGmac = []
    timeSubGmac1 = []
    timeSubGmac2 = []
    timeSubGmac3 = []
    numberOfGroups = [5, 10, 15, 20, 25]
    for i in numberOfGroups:
        gmac1 = gmac.GMAC(i, numberOfNodes)
        sub_gmac1 = sub_gmac.Sub_GMAC(i, numberOfNodes)
        eventInArea = [True, False, False, False, True, True, False, True, True, False,True, True, False, False, True, False, False, True, False, True, False, True, True, False, True]
        timeGmac.append(gmac1.run(eventInArea))
        timeSubGmac1.append(sub_gmac1.run2(eventInArea))
        timeSubGmac2.append(sub_gmac1.run3(eventInArea))
        timeSubGmac3.append(sub_gmac1.run4(eventInArea))


    timeG=np.array(timeGmac)
    timeSG=np.array(timeSubGmac1)
    timeSG2=np.array(timeSubGmac2)
    timeSG3=np.array(timeSubGmac3)
    groups=np.array(numberOfGroups)
    print(timeG, timeSG, groups)
    plt.plot(groups, timeG, label="GMAC")
    plt.plot(groups, timeSG, label="Sub GMAC, 2 Sub Groups")
    plt.plot(groups, timeSG2, label="Sub GMAC, 3 Sub Groups")
    plt.plot(groups, timeSG3, label="Sub GMAC, 4 Sub Groups")
    plt.xlabel("Number of Groups")
    plt.ylabel("Time (s)")
    plt.title("GMAC vs Sub GMAC")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()