import unittest
from sortPlanets import readFile, numOrphanPlanets, hottestStarPlanet, timeline

class TestPlanets(unittest.TestCase):
    def test_successful_response(self):
        result = readFile("https://gist.githubusercontent.com/joelbirchler/66cf8045fcbb6515557347c05d789b4a/raw/9a196385b44d4288431eef74896c0512bad3defe/exoplanets")
        self.assertTrue(isinstance(result, list))

    def test_not_found_response(self):
        with self.assertRaises(SystemExit):
            readFile("https://gist.githubusercontent.com/joelbirchle")
    
    def test_invalid_json_response(self):
        with self.assertRaises(SystemExit):
            readFile("https://gist.githubusercontent.com/joelbirchler")

    def test_empty_numOrphanPlanets(self):
        result = numOrphanPlanets([])
        self.assertEqual(result, 0)

    def test_none_numOrphanPlanets(self):
        data = [
            {"PlanetIdentifier": "ABC", "TypeFlag": 0},
            {"PlanetIdentifier": "DEF", "TypeFlag": 1},
            {"PlanetIdentifier": "HIJ", "TypeFlag": 2}
        ]
        result = numOrphanPlanets(data)
        self.assertEqual(result, 0)

    def test_all_numOrphanPlanets(self):
        data = [
            {"PlanetIdentifier": "ABC", "TypeFlag": 3},
            {"PlanetIdentifier": "DEF", "TypeFlag": 3},
            {"PlanetIdentifier": "HIJ", "TypeFlag": 3}
        ]
        result = numOrphanPlanets(data)
        self.assertEqual(result, 3)

    def test_nonint_numOrphanPlanets(self):
        data = [
            {"PlanetIdentifier": "ABC", "TypeFlag": ""},
            {"PlanetIdentifier": "DEF", "TypeFlag": 3},
            {"PlanetIdentifier": "HIJ", "TypeFlag": 3}
        ]
        result = numOrphanPlanets(data)
        self.assertEqual(result, 2)

    def test_empty_hottestStarPlanet(self):
        result = hottestStarPlanet([])
        self.assertEqual(result, [])

    def test_all_hottestStarPlanet(self):
        data = [
            {"PlanetIdentifier": "ABC", "HostStarTempK": 0},
            {"PlanetIdentifier": "DEF", "HostStarTempK": 0},
            {"PlanetIdentifier": "HIJ", "HostStarTempK": 0}
        ]
        result = hottestStarPlanet(data)
        self.assertEqual(result, ["ABC", "DEF", "HIJ"])

    def test_one_hottestStarPlanet(self):
        data = [
            {"PlanetIdentifier": "ABC", "HostStarTempK": 0},
            {"PlanetIdentifier": "DEF", "HostStarTempK": 2000},
            {"PlanetIdentifier": "HIJ", "HostStarTempK": 3}
        ]
        result = hottestStarPlanet(data)
        self.assertEqual(result, ["DEF"])
    
    def test_notint_hottestStarPlanet(self):
        data = [
            {"PlanetIdentifier": "ABC", "HostStarTempK": 0},
            {"PlanetIdentifier": "DEF", "HostStarTempK": ""},
            {"PlanetIdentifier": "HIJ", "HostStarTempK": 3}
        ]
        result = hottestStarPlanet(data)
        self.assertEqual(result, ["HIJ"])

    def test_empty_timeline(self):
        result = timeline([])
        self.assertEqual(result, [])

    def test_all_timeline(self):
        data = [
            {"PlanetIdentifier": "ABC", "DiscoveryYear": 1980, "RadiusJpt": 1},
            {"PlanetIdentifier": "DEF", "DiscoveryYear": 2000, "RadiusJpt": 2},
            {"PlanetIdentifier": "HIJ", "DiscoveryYear": 1980, "RadiusJpt": 0.54321}
        ]
        result = timeline(data)
        self.assertEqual(result[0].year, 1980)
        self.assertEqual(result[0].smPlanet, 1)
        self.assertEqual(result[0].medPlanet, 1)
        self.assertEqual(result[0].lgPlanet, 0)
        self.assertEqual(result[1].year, 2000)
        self.assertEqual(result[1].smPlanet, 0)
        self.assertEqual(result[1].medPlanet, 0)
        self.assertEqual(result[1].lgPlanet, 1)

    def test_nonint_timeline(self):
        data = [
            {"PlanetIdentifier": "ABC", "DiscoveryYear": 1980, "RadiusJpt": ""},
            {"PlanetIdentifier": "DEF", "DiscoveryYear": "", "RadiusJpt": 2},
            {"PlanetIdentifier": "HIJ", "DiscoveryYear": 2000, "RadiusJpt": 0.54321}
        ]
        result = timeline(data)
        self.assertEqual(result[0].year, 2000)
        self.assertEqual(result[0].smPlanet, 1)
        self.assertEqual(result[0].medPlanet, 0)
        self.assertEqual(result[0].lgPlanet, 0)

    def test_noyears_timeline(self):
        data = [
            {"PlanetIdentifier": "ABC", "DiscoveryYear": "", "RadiusJpt": 1},
            {"PlanetIdentifier": "DEF", "DiscoveryYear": "", "RadiusJpt": 2},
            {"PlanetIdentifier": "HIJ", "DiscoveryYear": "", "RadiusJpt": 0.54321}
        ]
        result = timeline(data)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
