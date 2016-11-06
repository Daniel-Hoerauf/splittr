from app import mongo
from bson.objectid import ObjectId
import re

def create_group(group_name, user_id):
    group = {
        'groupname': group_name,
        'members': {
            user_id: {}
        }
    }
    ID = mongo.db.groups.insert_one(group).inserted_id
    user = ObjectId(user_id)
    groups = mongo.db.users.find_one({'_id': user})['groups']
    groups.append(str(ID))
    mongo.db.users.update_one({'_id': user}, {'$set': {'groups': groups}})
    return str(ID)


def add_member_to_group(group_id, user_id):
    group_obj = ObjectId(group_id)
    user_obj = ObjectId(user_id)
    members = mongo.db.groups.find_one({'_id': group_obj})['members']
    if members.get(user_id):
        return False
    members[user_id] = {}
    mongo.db.groups.update_one({'_id': group_id}, {'$set': {'members': members}})
    groups = mongo.db.users.find_one({'_id': user_id})['groups']
    groups.append(group_id)
    mongo.db.users.update_one({'_id': user_id}, {'$set': {'groups': groups}})
    return True


def get_user_information(user_id):
    user_obj = ObjectId(user_id)
    info = mongo.db.users.find_one({'_id': user_obj}, {'groups': 1, 'username': 1})
    groups = info['groups']
    info['groups'] = [get_group_info(group) for group in groups]
    return info


def get_group_info(group_id):
    group_obj = ObjectId(group_id)
    return mongo.db.groups.find_one({'_id': group_obj}, {'groupname': 1,
                                                         '_id': 1,
                                                         'members': 1})


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
