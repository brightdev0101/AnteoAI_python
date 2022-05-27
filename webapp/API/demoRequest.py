import logging
from webapp.MailManager import MailManager
from webapp.API.Response import Response


def demoRequest(mail, name, company, brand):
    
    response = Response(True)      
    try:
        m = MailManager()
        m.sendDemo(mail, name, company, brand)
        response.status = True          
        
    except Exception as api_exception:
        response.status = False  
        logging.error("[setCustomTrend] API error - {}".format(api_exception))
        
        
    return response.compose()