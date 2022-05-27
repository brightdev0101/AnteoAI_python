import logging
from webapp.API.Response import Response

def getReport(ct_id): 
    """Get report API: create report for the custom trend (ct_id) and return an URL for download

    Params:
        data - User data to update
        current_user - User object Flask-Login


    Return:
        response - Composed response
    """

    try:
        # TODO >> [CustomTrend API] getReport
        # Create report for the custom trend (ct_id) and return an URL for download

        response = Response(True)           
        return response.compose()

        
    except Exception as api_exception:
        response = Response(False)     
        logging.error("[getReport] API error - {}".format(api_exception))