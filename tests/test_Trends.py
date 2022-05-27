import unittest, json

from webapp.API.getTrend import getTrend

class TrendsManagementTestCase(unittest.TestCase):

    def testLoad(self):
        result = getTrend("trends","it")
        result_dict = json.loads(result.data.decode('utf-8'))
        self.assertTrue(result_dict['status'])



