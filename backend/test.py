import unittest
import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_record(self):
        response = self.app.post('/get_record', json={"project_id": 1, "record_id": 1})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

if __name__ == '__main__':
    unittest.main()