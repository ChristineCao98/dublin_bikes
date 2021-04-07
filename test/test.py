from flask_app.routes import app
import unittest


class DBUnitTests(unittest.TestCase):
    def setUp(self):
        """creates a new test client and allows for the exceptions to propagate to the test client"""
        app.testing = True
        self.app = app.test_client()

    def test_index(self):
        """Test status code of the index"""
        response = self.app.get("/")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_stations_num(self):
        """Request and Parse The JSON response for stations"""
        # get_json() converts the JSON object into Python data
        response = self.app.get("/api/stations/").get_json()
        self.assertEqual(len(response), 1)

    def test_station_details(self):
        """Request and Parse the JSON response for the station details"""
        response = self.app.get("/api/stations/12").get_json()
        self.assertEqual(len(response), 1)

    def test_weather(self):
        """Request and Parse the JSON response for the weather information"""
        response = self.app.get("/api/weather/12").get_json()
        self.assertEqual(len(response), 8)

    def test_hourly(self):
        """Request and Parse the JSON response for the average hourly number of available bikes"""
        response = self.app.get("/api/hour/12").get_json()
        self.assertEqual(len(response), 24)

    def test_daily(self):
        """Request and Parse the JSON response for the average daily number of available bikes"""
        response = self.app.get("/api/day/12").get_json()
        self.assertEqual(len(response), 7)

    def test_prediction(self):
        """Request and Parse the JSON response for the prediction data of available bikes in the following 5 days"""
        response = self.app.get("/api/prediction/12").get_json()
        self.assertEqual(len(response), 6)


if __name__ == '__main__':
    unittest.main()
