import logging

from webapp.API.Response import Response
from webapp.dataobj.CustomTrend import CustomTrend
from webapp.vars import ERROR_API, SUCCESS_API

def setCustomTrend(ct_id, config):
    """Set Trend API: retrieve custom trend data and configuration

    Params:
        ct_id (integer) - Custom Trend ID
        config (object) - Custom Trend Configuration Object

    Return:
    response - Composed response
    """
    
    try:
        response = Response(True)   

        ct = CustomTrend()
        ct.ct_id = ct_id
        ct.config = config
        result = ct.saveConfig()

        if not result:
            response.status = False

        return response.compose()

        
    except Exception as api_exception:
        response = Response(False)     
        logging.error("[setCustomTrend] API error - {}".format(api_exception))
   
