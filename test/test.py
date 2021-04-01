from flask_app.routes import app
import unittest


# Test status code of index
class FlaskTestCase(unittest.TestCase):
    def test_idex(self):
        tester = app.test_client()
        response = tester.get("/")
        status_code = response.status_code
        self.assertEqual(status_code, 200)


if __name__ == "__main__":
    if __name__ == '__main__':
        unittest.main()
