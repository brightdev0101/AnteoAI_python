import json

from webapp.vars import TREND_ENTRYPOINT
from urllib.request import urlopen

class Trends():
    """Class for manage trends stats
    """

    def __init__(self):
        self.data = {}

    def loadData(self, filename):
        """Load trends data

        Return:
            result (boolean) - loading rtesult
        """

        try: 
            data_url = '{}{}.json'.format(TREND_ENTRYPOINT, filename)
            data_response = urlopen(data_url)
            self.data = json.loads(data_response.read())
            return True

        except Exception as e:
            return False
         
