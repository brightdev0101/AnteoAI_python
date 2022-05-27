class User():
    """ A class to represent a Anteo AI user
    Attributes:
		id              User identificator
        username        Username
        password        User password
        name            User name
        surname         User surname
        birthdate       User birthname
        email           User email
        plan            User subscription plan
        expire_plan     User subscription plan expiration
        newsletter      User newsletter subscription
		
    """

    def __init__(self, id , username, password='', name='', surname='', birthdate='', email='', plan='', expire_plan='', newsletter=None):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.email = email
        self.plan = plan
        self.expire_plan = expire_plan
        self.custom_trends = {}
        self.newsletter = None

    def toDictionary(self):
        """ A function that return all attribs in a dictionary

        Return:
            object (dictionary) - {attrib1: value1, attrib2: value2, . . . }
        """

        object_dict = {
            'username' : self.username,
            'password' : self.password,
            'name' : self.name,
            'surname' : self.surname, 
            'birthdate' : self.birthdate, 
            'email' : self.email,
            'plan': self.plan,
            'expire_plan': self.expire_plan,
            'custom_trends': self.custom_trends,
            'newsletter': self.newsletter,
        }
       
        return object_dict


    def is_active(self):
        """ Flask-login - all users are active
        """
        return True


    def get_id(self):
        """ Flask-login - use username as id
        """
        return self.username


    def is_authenticated(self):
        """ Flask-login - authentication flag
        """
        return True


    def is_anonymous(self):
        """ Flask-login - anonymous users aren't supported
        """
        return False

