import sys, os
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

import unittest
from main import app

class API_test(unittest.TestCase):
    def test_get_record_index(self):
        # data = {
        #     "project_id" : 86,
        #     "record_id":2
        # }
        # data = {
        #     "project_id" : 86
        # }

        data = {
            "user_id": "1",
            "project_status":"normal"
        }

        # response = self.client.post('/get_record_index', json=data)

        response = self.client.post('/project_index', json=data)

        # response = self.client.post('/tag_index', json=data)
        # response = self.client.post('/get_record', json=data)
        print(f"\n\nstatus code: {response.status_code}\ndata: {response.data.decode('utf-8')}\n")
        print(f"headers: {response.headers}")

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
