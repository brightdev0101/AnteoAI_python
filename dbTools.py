import time, os, json
from werkzeug.security import generate_password_hash
from webapp.DBManager import DBManager
from webapp.vars import DEFAULT_CT_CONFIG

def userInsert(username, password, email, name, surname, birthdate):
    try:
        db.open()
        db.insert('INSERT INTO users (username, password, email, name, surname, birthdate, plan, planExpire) VALUES (?,?,?,?,?,?,2,0)', (username, generate_password_hash(password), email, name, surname, birthdate))
        db.close()
        return True

    except Exception as e:
        print("INSERT QUERY FAILED - {}".format(e))
        return False


def userDelete(username):
    try:
        db.open()
        db.delete('DELETE FROM users WHERE username=?', (username,))
        db.close()
        return True

    except Exception as e:
        print("DELETE QUERY FAILED - {}".format(e))
        return False


def userUpdatePsw(username, new_password, new_plan):
    try:
        db.open()
        db.update('UPDATE users SET password=?, plan=? WHERE username=?', (generate_password_hash(new_password), new_plan, username))
        db.close()
        return True

    except Exception as e:
        print("UPDATE PASSWORD QUERY FAILED - {}".format(e))

def userShowTable():
    try:
        db.open()
        rows = db.select("SELECT * FROM users",())

        for row in rows:
            print(row)

        db.close()
        return True

    except Exception as e:
        print("USER SHOW TABLE ERROR - {}".format(e))


def customTrendInsert(user_id, title):
    try:
        db.open()
        result = db.insert('INSERT INTO customTrends (userId, title) VALUES (?,?)', (user_id, title))
        
        # Create new CT directory
        new_id = result[0]
        new_directory_path = "data/ct/{}/".format(new_id)
        os.mkdir(new_directory_path)
        
        # Add standard config json in the new CT folder
        new_config = DEFAULT_CT_CONFIG
        new_config["custom_trend_id"] = new_id
        
        with open("{}config.json".format(new_directory_path), 'w') as fp:
            json.dump(new_config, fp)
    
        db.close()
        return True

    except Exception as e:
        print("INSERT QUERY FAILED - {}".format(e))
        return False

def customTrendUpdate(id, title, user_id):
    try:
        db.open()
        db.update('UPDATE customTrends SET title=?, userId=? WHERE id=?', (title, user_id, id))
        db.close()
        return True

    except Exception as e:
        print("UPDATE PASSWORD QUERY FAILED - {}".format(e))

def customTrendDelete(id):
    try:
        db.open()
        db.delete('DELETE FROM customTrends WHERE id=?', (id,))
        db.close()
        return True

    except Exception as e:
        print("DELETE QUERY FAILED - {}".format(e))
        return False

def customTrendShowTable():
    try:
        db.open()
        rows = db.select("SELECT * FROM customTrends",())

        for row in rows:
            print(row)

        db.close()
        return True

    except Exception as e:
        print("USER SHOW TABLE ERROR - {}".format(e))



if __name__ == '__main__':
    
    db = DBManager()

    while True:
        print("")
        print("###################")
        print("#     Anteo AI    #")
        print("#     DB Tools    #")
        print("###################")
        print("")

        print("Menu:")
        print("1. [USER] INSERT")
        print("2. [USER] DELETE")
        print("3. [USER] UPDATE password")
        print("4. [USER] Show Table")
        print("5. [CUSTOM TREND] INSERT")
        print("6. [CUSTOM TREND] DELETE")
        print("7. [CUSTOM TREND] UPDATE")
        print("8. [CUSTOM TREND] Show Table")
        print("q. Quit")
        print("")

        query = input("Choose & Enter query number available in the menu: ")

        if query == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            email = input("Enter email address: ")
            name = input("Enter name: ")
            surname = input("Enter surname: ")
            birthdate = input("Enter birthdate: ")
            userInsert(username, password, email, name, surname, birthdate)

        elif query == "2":
            username = input("Enter username: ")
            userDelete(username)

        elif query == "3":
            username = input("Enter username: ")
            new_password = input("Enter new password: ")
            new_plan = int(input("Enter New Plan ID: "))
            userUpdatePsw(username, new_password, new_plan)

        elif query == "4":
            userShowTable()

        elif query == "5":
            user_id = input("User ID: ")
            title = input("Title: ")
            customTrendInsert(user_id, title)

        elif query == "6":
            delete_id = input("Delete ID: ")
            customTrendDelete(delete_id)

        elif query == "7":
            id = input("Trend ID: ")
            title = input("New Title: ")
            user_id = input("New User ID: ")
            customTrendUpdate(id, title, user_id)

        elif query == "8":
            customTrendShowTable()

        elif query == "q":
             break

        else:
            print("Command not recognized, try again!")
            time.sleep(3)

    