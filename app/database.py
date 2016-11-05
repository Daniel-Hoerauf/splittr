from app import mongo
import re


def register_user(username, password, email):
    user = {
        'username': username,
        'password': password,
        'email': email,
        'groups': []
    }
    ID = mongo.db.users.insert_one(user).inserted_id
    return str(ID)


def login_user(username, password):
    user = mongo.db.users.find_one({'username': username, 'password': password})
    if user:
        return str(user['_id'])
    else:
        return False


def search_user(user_snippet):
    if user_snippet == '':
        results = mongo.db.users.find({}, {'username': 1})
    else:
        re_string = re.compile(user_snippet, re.I)
        results = mongo.db.users.find({'username': re_string}, {'username': 1})
    ret = []
    for user in results:
        ret.append({'username': user['username'], 'id': str(user['_id'])})
    results.close()
    return ret


def check_username_avail(username):
    user = mongo.db.users.find_one({'username': username})
    if user:
        return False
    else:
        return True
