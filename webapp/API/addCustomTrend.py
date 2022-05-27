import logging

from webapp.API.Response import Response
from webapp.dataobj.CustomTrend import CustomTrend
from webapp.vars import ERROR_API, SUCCESS_API

def addCustomTrend(userId, title):
    """Add a new Custom Trend API

    Params:
        userId (integer) - User ID
        title (string) - Trend title

    Return:
        response - Composed response
    """
    
    try:
        response = Response(True)   

        ct = CustomTrend()
        new_id = ct.add(userId, title)

        if not new_id or new_id == "":
            raise Exception()
            
        response.add("ctid", new_id)
        return response.compose()

    except Exception as api_exception:
        response = Response(False)     
        logging.error("[addCustomTrend] API error - {}".format(api_exception))
