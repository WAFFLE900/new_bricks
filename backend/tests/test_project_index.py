import sys, os
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

import unittest
from main import app

class API_test(unittest.TestCase):
    def test_project_index(self):
        data = {
            "user_id": "1",
            "project_status":"normal"
        }
        response = self.client.post('/project_index', json=data)
        print(response.data.decode('utf-8'))

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.ctx = app.app_context()
        cls.ctx.push()

    @classmethod
    def tearDownClass(cls):
        cls.ctx.pop()
        

if __name__ == '__main__':
    unittest.main()
