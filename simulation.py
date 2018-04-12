from analyzeRelevantCrimes import main

class District:
    def __init__(self, security, attractiveness):
        self.security = security
        self.attractiveness = attractiveness

class Location:
    # Initialize object with given values
    def __init__(self, wealth, security, attractiveness):

        self.wealth = wealth
        self.security = security
        self.baseAttractiveness = attractiveness

class Police:
    # Initialize object with given values
    def __init__(self):
        pass

class Thief:
    # Initialize object with given values
    def __init__(self, riskAversion, need):
        self.riskAversion = riskAversion
        self.need = need

# Make list of house objects
# If going further, a list/dict where each entry corresponds to a district and is a list of houses for that district


numIncidents, numArrests, descriptions, districts = main()
# Districts looks like:
# District: {'Arrests', 'Incidents', 'Locations:{'block1': {'Arrests', 'Incidents'}, etc. } }
