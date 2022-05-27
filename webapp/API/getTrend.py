import logging, json

from webapp.API.Response import Response
from webapp.dataobj.Trends import Trends

def getTrend(trend_id, lang):
    """Get new home trends API

    Params:
        trend_id (int) - Trend ID (1 > TRENDS - 2 > FINANCE - 3 > SPORT . . .)
        lang (string) - Trend language

    Return:
        response - Composed response
    """

    try:
        response = Response(True)

        #Compose filename
        filename = "{}-{}".format(trend_id, lang) 
        
        # Retrieve Data
        trends = Trends()
        load_result = trends.loadData(filename)
        
        if load_result:
            response.add("data", trends.data)
        else:
            response.status = False
                  
        return response.compose()
       
    except Exception as api_exception:
        response = Response(False)     
        logging.error("[getTrends] API error - {}".format(api_exception))
        return response.compose()
 
  
