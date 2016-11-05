from app import mongo

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
