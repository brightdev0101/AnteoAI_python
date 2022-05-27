from werkzeug.security import generate_password_hash, check_password_hash
from webapp import signin
from webapp.DBManager import DBManager
from webapp.vars import SQL_DB
from webapp.User import User

@signin.user_loader
def load_user(username):
    db = DBManager()

    # Retrieve user details
    db.open()
    users = db.select('SELECT * FROM users WHERE username=?',(username,))

    if len(users) > 0:
        user_id = users[0][0]
        email = users[0][3]
        name = users[0][4]
        surname = users[0][5]
        birthdate = users[0][6]
        plan = users[0][7]
        expire_plan = users[0][8]
        newsletter = users[0][9]
        user = User(user_id, username, '', name, surname, birthdate, email, plan, expire_plan, newsletter)


        # Retrieve custom trends
        db.close()
        db.open()
        custom_trends = db.select('SELECT * FROM customTrends WHERE userId=?', (user_id,))
        for trend in custom_trends:
            user.custom_trends[trend[0]] = trend[2]

        return user
    return None


class UsersManager():
    """ Users management interface
    Attributes:
        user (User)     The user object
        db (DBManager)  The database manager object
    """

    def __init__(self, user=None):
        self.user = user
        self.db = DBManager()
        self.FIRSTPOS = 0
        self.LASTPOS = 2


    def fetch(self):
        """ Check if user are in DB
        Return:
            result (boolean)
        """
        self.db.open()
        results = self.db.select('SELECT username FROM users WHERE username=?', (self.user.username,))

        if len(results) > 0:
            return True
        else:
            return False


    def check(self):
        """ Check if user/pwd are in DB
        Return:
            result (boolean)
        """
        self.db.open()
        results = self.db.select(
            'SELECT * FROM users WHERE username=?', (self.user.username,))

        if len(results) > 0:
            if check_password_hash(results[self.FIRSTPOS][self.LASTPOS], self.user.password):
                return True

        return False


    def add(self):
        """ Add a new user
        Return:
            (result (boolean), errors (string))
        """
        self.db.open()
        return self.db.insert('INSERT INTO users (username,password,name,surname,birthdate,email,newsletter) VALUES (?,?,?,?,?,?)', (self.user.username, generate_password_hash(self.user.password), self.user.name, self.user.surname, self.user.birthdate, self.user.email, self.user.newsletter))


    def remove(self):
        """ Remove a user
        Return:
            (result (boolean), errors (string))
        """
        self.db.open()
        return self.db.delete('DELETE FROM users WHERE username=?', (self.user.username,))


    def update(self, name, surname, email, birthdate, newsletter):
        """ Update user details
        Params:
            name - Name of user (string)
            surname - Surname of user (string)
            email - Email of user (string)
            birthdate - Birthdate of user (date)
            newsletter - Newsletter Subscription flag (integer)
        Return:
            (result (boolean), errors (string))
        """
        result = True
        error = ""

        self.db.open()
        result, error = self.db.update('UPDATE users SET name=?,surname=?,email=?,birthdate=?, newsletter=? WHERE username=?', (
            name, surname, email, birthdate, newsletter, self.user.username))
        if not result:
            return (result, error)

        return (result, error)

    def newPassword(self, newpwd):
        """ Update user password
        Params:
            username (string)
            newpwd (string) - New Password
        Return:
            (result (boolean), errors (string))
        """

        result = True
        error = ""

        self.db.open()
        result, error = self.db.update('UPDATE users SET password=? WHERE username=?', (generate_password_hash(newpwd), self.user.username))
        if not result:
            return (result, error)

        return (result, error)

    def getAll(self):
        """ Get all users in DB
        Return:
            users (Array[User])
        """
        users_list = []

        self.db.open()
        results = self.db.select('SELECT username, id FROM users', ())

        for result in results:
            tmp_user = User(username = result[0], id = result[1])
            users_list.append(tmp_user)

        return users_list


    def currentUser(self):
        user = load_user(self.user.username)
        return user

