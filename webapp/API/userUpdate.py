import logging
from webapp.UsersManager import UsersManager

def userUpdate(data, current_user):
    """User Update API

    Params:
        data - User data to update
        current_user - User object Flask-Login


    Return:
        response - Composed response
    """

    try:
        manager = UsersManager(current_user)

        if current_user is not None:
            manager.update(data['name'], data['surname'], data['email'], data['birthdate'])
  
    except Exception as api_exception:  
        logging.error("[userUpdate] API error - {}".format(api_exception))
   
