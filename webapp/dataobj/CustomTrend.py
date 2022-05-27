import json, time, shutil
import os, errno
from urllib.request import urlopen

from webapp.DBManager import DBManager
from webapp.vars import CUSTOM_TREND_DIR, DATA_ENTRYPOINT

class CustomTrend():
    """A class to manage customized trend search
    All custom trends are stored in CUSTOM_TREND_DIR (Path: data/ct/ct_id).
    Every custom trend folder must have a config.json file and a data_x.json file.
    """


    def __init__(self, ct_id = None):
        self.ct_id = ct_id
        self.config = None
        self.data = None
        self.db = DBManager()

    def delete(self):
        """ Delete custom trend
        N.B. The ct_id must be setted

        Return:
            result (boolean) - loading result
        """
        self.db.open()
        result = self.db.delete('DELETE FROM customTrends WHERE id=?', (self.ct_id,))
        self.db.close()
        return result

    def add(self, user_id, title):
        """ Add a new custom trend

        Return:
            new_id (integer) - New custom trend id
        """
        self.db.open()
        new_id, _ = self.db.insert('INSERT INTO customTrends (userId, title) VALUES (?,?)', (user_id, title))
        self.db.close()

        filename = "{}{}/config.json".format(CUSTOM_TREND_DIR, new_id)
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except Exception as e:
                raise

        with open("{}{}/config.json".format(CUSTOM_TREND_DIR, new_id), 'w') as f:
            default_config = {
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
                "custom_trend_id": new_id,
                "key": title
            }
            json.dump(default_config, f)

        
        self.ct_id = new_id
        return new_id


    def loadConfig(self, ct_id):
        """Load custom trend configuration from file

        Params:
            ct_id (integer) - custom trend ID
        Return:
            result (boolean) - loading result
        """

        self.ct_id = ct_id
        
        with open("{}{}/config.json".format(CUSTOM_TREND_DIR, self.ct_id)) as f:
            self.config = json.load(f)
            return True

        return False


    def loadData(self):
        """Load custom trend data. 
        N.B. Before this operation configuration must be loaded.

        Return:
            result (boolean) - loading result
        """
        
        try: 
            data_url = '{}{}/data.json'.format(DATA_ENTRYPOINT, self.ct_id)
            data_response = urlopen(data_url)
            self.data = json.loads(data_response.read())
            return True

        except Exception as e:
            return False
            

    def saveConfig(self):
        """Save current configuration to config.json file. 
        N.B. Before this operation configuration must be loaded.

        Return:
            result (boolean) - saving result
        """

        if self.ct_id != None and self.config != None and self.config:
            with open("{}{}/config.json".format(CUSTOM_TREND_DIR, self.ct_id), 'w') as f:
                json.dump(self.config, f)
                
                self.db.open()
                self.db.update('UPDATE customTrends SET title=?WHERE id=?', (self.config['key'], self.config['custom_trend_id']))
                self.db.close()

                return True

        return False 
