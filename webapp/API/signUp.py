import logging
from webapp.API.Response import Response
from webapp.UsersManager import UsersManager
from webapp.vars import ERROR_API

def signUp(current_user, message):
    """User Registration API

    Params:
        current_user - User object Flask-Login
        message - Result message status 


    Return:
        response - Composed response
    """

    try:
        response = Response(True)
        manager = UsersManager(current_user)

        if current_user is not None:
            if message == 'Password unmatching':
                response.status = False
                response.message = message
                return response.compose()

            if manager.fetch():
                message = 'User already exists'
                response.status = False

            else:
                manager.add()

            response.data = {
                'username': current_user.username,
                'password': current_user.password,
                'name': current_user.name,
                'surname': current_user.surname,
                'birthdate': current_user.birthdate,
                'email': current_user.email                
            }
            response.message = message

        else:
            response.status = False
            response.message = ERROR_API

        return response.compose()
        
    except Exception as api_exception:
        response = Response(False)     
        logging.error("[signUp] API error - {}".format(api_exception))
   
