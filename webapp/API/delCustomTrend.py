import logging

from webapp.API.Response import Response
from webapp.dataobj.CustomTrend import CustomTrend
from webapp.vars import ERROR_API, SUCCESS_API

def delCustomTrend(ct_id):
    """Delete Custom Trend API: delete a trend

    Params:
        ct_id (integer) - Custom Trend ID

    Return:
        response - Composed response
    """
    
    try:
        response = Response(True)   

        ct = CustomTrend(ct_id)
        result = ct.delete()

        if not result:
            raise Exception()
            
        return response.compose()

    except Exception as api_exception:
        response = Response(False)     
        logging.error("[delCustomTrend] API error - {}".format(api_exception))
