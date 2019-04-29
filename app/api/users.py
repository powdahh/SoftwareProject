from app.api import api
from app import Database
import mysql.connector
import json


@api.route('/create_user', methods=['POST'])
def create_user(user_info):
    data = json.loads(user_info)
    email = data["email"]
    userName = data["userName"]
    passwordHash = data["passwordHash"]
    fullName = data["fullName"]

    myDb = Database.dbConnection()
    print(myDb)
    sqlString = ""
    values = (email, userName, passwordHash, fullName)
    result = Database.execStatement(myDb, sqlString, values)
    myDb.commit()
    #return(result)



@api.route('/check_user',methods=['GET'])
def check_user(user_info):
    data = json.loads(user_info)
    email = data["email"]
    userName = data["userName"]

    myDb = Database.dbConnection()
    print(myDb)
    sqlString_Email = "SELECT email FROM users WHERE email = " + "'" + email + "'"
    sqlString_UserName = "SELECT userName FROM users WHERE userName = " + "'" + userName + "'"
    result1 = Database.selectStatement(myDb, sqlString_Email)
    result2 = Database.selectStatement(myDb, sqlString_UserName)
    if (result1.rowcount != 0):
        return 'email taken'
    elif (result2.rowcount != 0):
        return 'username taken'
    else:
        return 'clear'




@api.route('/get_user', methods=['GET'])
def get_user(login_info):
    data = json.loads(login_info)
    email = data["email"]
    passwordHash = data["passwordhash"]

    myDb = Database.dbConnection()
    print(myDb)
    sqlString = "SELECT passwordHash, userid FROM users WHERE email = " + "'" + email + "'"
    result = Database.selectStatement(myDb, sqlString)
    if(result.rowcount == 1):
        fetch = result.fetchone()
        if (fetch[0] == passwordHash):
            return fetch[1]
    else:
        return False

@api.route('/get_subscribers', methods=["GET"])
def get_subscribers():
    myDb = Database.dbConnection()
    print(myDb)
    sqlString = "SELECT email FROM users WHERE isSubscribed = '1'"
    result = Database.selectStatement(myDb, sqlString)
    fetch = result.fetchall()
    emailList = []
    for i in fetch:
        emailList.append(i[0])
    return emailList

@api.route('/update_name', methods=["GET"])
def update_name(update_info):
    data = json.loads(update_info)
    name = data["name"]
    userid = str(data["userid"])
    myDb = Database.dbConnection()
    print(myDb)
    sqlString = "UPDATE users SET fullname = " + "'" + name + "'" + "WHERE userid = " + "'" + userid + "'"
    result = Database.selectStatement(myDb, sqlString)
    myDb.commit()

@api.route('/update_subscription', methods=["GET"])
def update_subscription(update_info):
    data = json.loads(update_info)
    status = str(data["status"])
    userid = str(data["userid"])
    myDb = Database.dbConnection()
    print(myDb)
    sqlString = "UPDATE users SET isSubscribed = " + "'" + status + "'" + "WHERE userid = " + "'" + userid + "'"
    result = Database.selectStatement(myDb, sqlString)
    myDb.commit()

@api.route('/get_user_info', methods=["GET"])
def get_user_info(info):
    data = json.loads(info)
    userid = str(data["userid"])
    myDb = Database.dbConnection()
    print(myDb)
    sqlString = "SELECT username, fullname, isSubscribed FROM users WHERE userid = " + "'" + userid + "'"
    result = Database.selectStatement(myDb, sqlString)
    fetch = result.fetchall()
    user_info = {
        "username": fetch[0][0],
        "fullname": fetch[0][1],
        "isSubscribed": fetch[0][2]
    }
    return json.dumps(user_info)

@api.route('/change_password', methods=["GET"])
def change_password(info):
    data = json.loads(info)
    current_hash = data["current_hash"]
    change_hash = data["change_hash"]
    userid = str(data["userid"])
    myDb = Database.dbConnection()
    print(myDb)
    sqlString = "UPDATE users SET passwordHash = " + "'" + change_hash + "'" + "WHERE userid = " + "'" + userid + "'" + "AND passwordHash = " + "'" + current_hash + "'"
    result = Database.selectStatement(myDb, sqlString)
    myDb.commit()




