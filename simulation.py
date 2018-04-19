import operator
import random
import math
import numpy as np
import pprint
pp = pprint.PrettyPrinter()

from analyzeRelevantCrimes import main

class District:
    def __init__(self, name, wealthModifier, security, attractiveness, incidents):
        self.name = name
        self.wealthModifier = wealthModifier
        self.security = security
        self.attractiveness = attractiveness
        self.incidents = incidents
        self.locations = []
    
    def addChild(self, location):
        self.locations.append(location)
    
    def getTotalLocations(self):
        self.totalLocations = len(self.locations)
        return self.totalLocations
    

class Location:
    # Initialize object with given values
    def __init__(self, wealth, security, attractiveness, parentDistrict):
        self.wealth = wealth
        self.security = security
        self.baseAttractiveness = attractiveness
        self.parentDistrict = parentDistrict

class Police:
    # Initialize object with given values
    def __init__(self):
        pass

class Thief:
    # Initialize object with given values
    def __init__(self, riskAversion, need):
        self.riskAversion = riskAversion
        self.need = need
    
    def randomRiskAversion(self):
        randomNum = random.gauss(2, 1)
        if randomNum < 0:
            randomNum = 0

# Call main from analyzeRelevantCrimes
numIncidents, numArrests, descriptions, parsedDistricts = main()
# Districts look like:
# District: {'Arrests', 'Incidents', 'Locations:{'block1': {'Arrests', 'Incidents'}, etc. } }

# Make a sorted list of tuples from the districts
sortedParsedDistricts = sorted(parsedDistricts.items(), key=operator.itemgetter(0))
#pp.pprint(sortedParsedDistricts)

districtObjs = []
locationObjs = []

# Note that the district numbers go from 001 to 025, excluding 013, 021, and 023
for district in sortedParsedDistricts:
    name = district[0]
    numLocations = len(district[1]["Locations"])
    districtIncidents = district[1]["Incidents"]
    
    baseSecurity = numLocations / districtIncidents
    baseAttractiveness = districtIncidents / numLocations

    # This function decreases as the incidents get larger, but is always increasing for locations
    # (Increase denomenator for lower multipliers or vice versa)
    wealthModifier = (numLocations * math.log10(numLocations)) / (0.2 * districtIncidents)

    thisDist = District(name, wealthModifier, baseSecurity, baseAttractiveness, districtIncidents)
    districtObjs.append(thisDist)

    for location, values in district[1]["Locations"].items():
        locationAttractiveness = values["Incidents"]
        locationSecurity = values["Arrests"] / values["Incidents"] if "Arrests" in values else 0

        # Calculate random wealth for each houshold based on a pareto distribution
        # This makes most locations in a district have roughly similar wealth
        baseBeforeModifier = 10000
        baseAfterModifier = baseBeforeModifier * wealthModifier
        locationWealth = np.random.pareto(0.01) + baseAfterModifier
        # There is no upper bound on pareto distribution, so if it is too high recalculate for a lower wealth
        while True:
            if locationWealth > baseAfterModifier * 10:
                locationWealth = np.random.pareto(0.01) + baseAfterModifier
            else:
                break

        thisLocation = Location(int(locationWealth), locationSecurity, locationAttractiveness, thisDist)
        #locationObjs.append(thisLocation)
        thisDist.addChild(thisLocation)


totalAvg = 0
for i in districtObjs:
    print()
    print("District", i.name, "locations:", i.getTotalLocations(), "   incidents:", i.incidents)
    print("Average incidents per location:", round(i.incidents/i.getTotalLocations(), 2))
    print("District wealth modifier", round(i.wealthModifier, 2))
    total = sum(j.wealth for j in i.locations)
    print("District", i.name, "average wealth:", round(total/i.getTotalLocations(), 2))
    totalAvg += total/i.getTotalLocations()

print()
print("Total average income:", totalAvg/len(districtObjs))
# for district in districtObjs:
#     print("District:", district.name)
#     print("Security:", district.security)
