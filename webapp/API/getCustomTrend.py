import logging, json
from urllib.request import urlopen

from webapp.API.Response import Response
from webapp.dataobj.CustomTrend import CustomTrend



def getCustomTrend(ct_id):
    """Custom Trend API: retrieve custom trend data and configuration

    Params:
        ct_id (integer) - Custom Trend ID

    Return:
        ct (object) - {"config": {...}, "data": {...}}
    """

    try:
        response = Response(True)
        ct = CustomTrend()
        ct.loadConfig(ct_id)
        load_result = ct.loadData()

        if load_result:
            response.add("config", ct.config)
            response.add("data", ct.data)
        else:
            response.status = False
                  
        return response.compose()
       
    except Exception as api_exception:
        response = Response(False)     
        logging.error("[getCustomTrend] API error - {}".format(api_exception))
        return response.compose()
   
