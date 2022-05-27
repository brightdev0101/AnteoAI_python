import logging
from webapp.API.Response import Response
from webapp.UsersManager import UsersManager
from webapp.vars import ERROR_API, SUCCESS_API

def getUser(current_user):
    """Get user informations API

    Params:
        current_user - User object Flask-Login


    Return:
        response - Composed response
    """


    try:
        response = Response(True)
        manager = UsersManager(current_user)
        user = manager.currentUser()

        if user is not None:
            response.data = {
                'username': user.username,
                'name': user.name,
                'surname': user.surname,
                'email': user.email,
                'birthdate': user.birthdate,
                'plan': user.plan,
                'expire_plan': user.expire_plan,
                'preferred_topics': user.preferred_topics,
                'custom_trends': user.custom_trends,
                "subscription_newsletter": user.subscription_newsletter,
                "subscription_alert": user.subscription_alert,
                "subscription_features_newsletter": user.subscription_features_newsletter,
                "source_tw": user.source_tw,
                "source_ig": user.source_ig,
                "source_gogl": user.source_gogl
            }
            response.message = SUCCESS_API

        else:
            response.status = False
            response.message = ERROR_API

        return response.compose()
        
    except Exception as api_exception:
        response = Response(False)     
        logging.error("[getUser] API error - {}".format(api_exception))
   
