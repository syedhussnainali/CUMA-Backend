from flask import session

def getSessionUserID():
    user_id = session['user_id']
    #print(user_id)
    return user_id