import requests

def readFile(url):
    # send an http request to get the json data from the given url
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            return(data)
        except:
            print("Error. Url data is not in a json format.")
            exit()
    else:
        print("Error. Status code: {0}".format(response.status_code))
        exit()
    

def numOrphanPlanets(data):
    result = 0
    # iterate through each planet in the data to check that the TypeFlag is set to 3 (defines orphan planets)
    for planet in data:
        if planet["TypeFlag"] == 3:
            result +=1
    return result

def hottestStarPlanet(data):
    hottestTemp = 0
    result = []
    # iterate through each planet in the data to find the hottest star temp
    for planet in data:
        if type(planet["HostStarTempK"]) == float or type(planet["HostStarTempK"]) == int:
            if planet["HostStarTempK"] > hottestTemp:
                # update the hottest temp found so far
                hottestTemp = int(planet["HostStarTempK"])
    # go back through the list and add all planets with the hottest star temp to the result
    for planet in data:
        if planet["HostStarTempK"] == hottestTemp:
            result.append(planet["PlanetIdentifier"])
    return result

# create a class for storing the data for each year in the timeline
class Timeline:
    def __init__(self, year, smPlanet, medPlanet, lgPlanet):
        self.year = year
        self.smPlanet = smPlanet
        self.medPlanet = medPlanet
        self.lgPlanet = lgPlanet

def timeline(data):
    minYear = 10000
    maxYear = 0
    result = []
    # find the min year and max year to iterate through
    for planet in data:
        if type(planet["DiscoveryYear"]) == int:
            if planet["DiscoveryYear"] < minYear:
                minYear = planet["DiscoveryYear"]
            if planet["DiscoveryYear"] > maxYear:
                maxYear = planet["DiscoveryYear"]
    # iterate through the years; finding the number of small, medium, and large planets for each year
    for year in range(minYear, maxYear+1):
        smPlanet = 0
        medPlanet = 0
        lgPlanet = 0
        for planet in data:
            if planet["DiscoveryYear"] == year:
                if type(planet["RadiusJpt"]) == float or type(planet["RadiusJpt"]) == int:
                    if planet["RadiusJpt"] < 1:
                        smPlanet +=1
                    elif planet["RadiusJpt"] < 2:
                        medPlanet +=1
                    else:
                        lgPlanet +=1
        # only add the year and data if there were any discoveries
        if smPlanet != 0 or medPlanet != 0 or lgPlanet != 0:
            result.append(Timeline(year, smPlanet, medPlanet, lgPlanet))
    return result

if __name__ == "__main__":
    # get data from url
    url = "https://gist.githubusercontent.com/joelbirchler/66cf8045fcbb6515557347c05d789b4a/raw/9a196385b44d4288431eef74896c0512bad3defe/exoplanets"
    data = readFile(url)

    # find number of orphan planets (no star)
    numOP = numOrphanPlanets(data)
    if numOP == 1:
        print("There is {0} orphan planet.".format(numOP))
    else:
        print("There are {0} orphan planets.".format(numOP))

    # find name (planet identifier) of the planet orbiting the hottest star
    hsPlanet = hottestStarPlanet(data)
    if len(hsPlanet) == 0:
        print("There is not enough data to determine which planet is orbiting the hottest star.")
    elif len(hsPlanet) == 1:
        print("{0} is orbiting the hottest star.".format(hsPlanet[0]))
    else:
        print("{0} are orbitting the hottest star.".format(hsPlanet))

    # timeline of the number of planets discovered per year grouped by size
    timelinePlanets = timeline(data)
    if len(timelinePlanets) == 0:
        print("There is not enough data to create a timeline of planet discovery.")
    else:
        for time in timelinePlanets:
            print("In {0} we discovered {1} small planets, {2} medium planets, and {3} large planets.".format(time.year, time.smPlanet, time.medPlanet, time.lgPlanet))
