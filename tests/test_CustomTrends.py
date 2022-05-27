import unittest, json

from webapp.API.getCustomTrend import getCustomTrend
from webapp.API.addCustomTrend import addCustomTrend
from webapp.API.delCustomTrend import delCustomTrend
from webapp.API.setCustomTrend import setCustomTrend

class CustomTrendManagementTestCase(unittest.TestCase):

    def testCreate(self):
        # Create a new custom trend
        result = addCustomTrend(1, "UnitTest CT")
        result_dict = json.loads(result.data.decode('utf-8'))
        self.assertTrue(result_dict['status'])



    def testEdit(self):
        # Edit custom trend 1
        DEMO_ID = 1
        config = {
                "custom_config": {
                    "alert_influencers": True,
                    "alert_sentiment": True,
                    "alert_trends": True,
                    "algorithm": 1,
                    "analysis_emoji": True,
                    "analysis_images": True,
                    "analysis_text": True,
                    "georeference": "it",
                    "keywords": "",
                    "language": "it",
                    "main_param": 1,
                    "plot1": "bar_sentiment",
                    "plot2": "bar_sentiment",
                    "plot3": "bar_sentiment",
                    "source_gogl": True,
                    "source_ig": True,
                    "source_tw": True,
                    "timeframe": 7,
                    "report": 1
                },
                "custom_trend_id": "",
                "key": "UnitTest CT Edited"
            }

        result = setCustomTrend(DEMO_ID, config)
        result_dict = json.loads(result.data.decode('utf-8'))
        self.assertTrue(result_dict['status'])

   
    def testLoad(self):
        # Load the demo custom trend
        DEMO_ID = 1
        result = getCustomTrend(DEMO_ID)
        result_dict = json.loads(result.data.decode('utf-8'))
        self.assertTrue(result_dict['status'])

    def testDelete(self):
        result = delCustomTrend(1)
        result_dict = json.loads(result.data.decode('utf-8'))
        self.assertTrue(result_dict['status'])

        

