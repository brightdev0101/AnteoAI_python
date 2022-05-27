import logging
from webapp.API.Response import Response
from webapp.UsersManager import UsersManager
from webapp.vars import ERROR_API

def signIn(current_user, message):
    """User Login API

    Params:
        current_user - User object Flask-Login
        message - Result message status 


    Return:
        response - Composed response
    """


    try:
        response = Response(True)
        manager = UsersManager(current_user)
        user = manager.currentUser()

        if current_user is not None:
            response.data = user.toDictionary()
            response.message = message
            
            if not manager.check():
                response.status = False                

        else:
            response.status = False
            response.message = ERROR_API

        return response.compose()
        
    except Exception as api_exception:
        response = Response(False)     
        logging.error("[signIn] API error - {}".format(api_exception))
   
