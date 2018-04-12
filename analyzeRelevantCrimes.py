
def main():
    import csv
    # from PyQt5.QtWidgets import QApplication, QWidget
    # from PyQt5 import QtGui

    # class Window(QtGui.QMainWindow()):
    #     def __init__(self):
    #         super(Window, self).__init__()
    #         self.setGeometry(50, 50, 500, 500)
    #         self.setWindowTitle("Theft Simulation")
    #         self.show()

    # app = QtGui.QGuiApplication([])
    # GUI = Window()

    # Add key to dictionary if it doesn't exist. Increment it by 1 if it does exist.
    def populateDict(thisDict, key, boolArrest):
        if key not in thisDict:
            thisDict[key] = {"Incidents":1}
        else:
            thisDict[key]["Incidents"] +=1
        if boolArrest:
            addKeyToDict(thisDict, key, "Arrests")

    def addKeyToDict(thisDict, key, keyToAdd):
        if keyToAdd not in thisDict[key]:
            thisDict[key][keyToAdd] = 1
        else:
            thisDict[key][keyToAdd] += 1

    # Globals that will be populated while iterating through data
    numIncidents = 0
    numArrests = 0
    descriptions = {}
    districts = {}

    with open('Relevant_Crimes.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = list(reader)

        numIncidents = len(data) - 1    # First entry is headers

        first = 1
        print("Total rows:", len(data))
        for i in data:
            # Each entry (i) should look like this:
            # i[ 0   1            2     3      4            5                     6       7     8         9    ]
            #  [ ID, Case number, Date, Block, Description, Location Description, Arrest, Beat, District, Year ]
            if first == 1:
                first = 0
                continue

            # If arrest was made, increment. Also set boolean value based on arrest
            if i[6] == "true":
                numArrests += 1
                arrest = 1
            else:
                arrest = 0

            # Populate dicts with relevant data, number of incidents, and number of arrests
            populateDict(descriptions, i[4], arrest)
            populateDict(districts, i[8], arrest)
            if "Locations" not in districts[i[8]]:
                districts[i[8]]["Locations"] = {}
                populateDict(districts[i[8]]["Locations"], i[3], arrest)
            else:
                populateDict(districts[i[8]]["Locations"], i[3], arrest)
            # Districts looks like:
            # District: {'Arrests', 'Incidents', 'Locations:{'block1': {'Arrests', 'Incidents'}, etc. } }

    return numIncidents, numArrests, descriptions, districts

if __name__ == '__main__':
    import pprint
    pp = pprint.PrettyPrinter()

    numIncidents, numArrests, descriptions, districts = main()

    print("Total incidents:", numIncidents)
    print("Number of arrests:", numArrests)
    print("Arrest/incident ratio:", numArrests/numIncidents)

    #pp.pprint(locations)
    # pp.pprint(descriptions)
    #pp.pprint(districts)

    # for key, values in districts.items():
    #     print()
    #     print("District", key, ":")
    #     print("Total incidents:", values["Incidents"])
    #     print("Total locations:", len(values["Locations"]))
    #     print("Locations/incidents (higher is better):", len(values["Locations"])/values["Incidents"])
    
    # for key, values in districts.items():
    #     arrestRatio = values["Arrests"] / values["Incidents"]
    #     print(key, "arrest ratio:", arrestRatio)

    print()
    print("Done.")