import pymongo
from bson.objectid import ObjectId

db = pymongo.Connection().fujiwara

users = db.users.find()

for i in users:
    new_user = {}
    new_user['name'] = i['user']
    new_user['name_lower'] = i['_un_lower']
    new_user['email'] = i['email']
    new_user['hashed_pwd'] = i['pwd']
    new_user['_id'] = i['_id']

    if i['group'] == 'admin':
        new_user['jobs'] = ['admin']
    else:
        new_user['jobs'] = []

    db.users.update({'_id':new_user['_id']},
                     new_user)

threads = db.threads.find()

for i in threads:
    new_thread = i
    new_thread['author'] = new_thread['author_id']
    del new_thread['author_id']

    db.threads.update(
        {'_id':new_thread['_id']},
        new_thread
    )

posts = db.posts.find()

for i in posts:
    new_posts = i
    new_posts['author'] = i['author_id']
    del new_posts['author_id']
    new_posts['th'] = ObjectId(new_posts['th'])
    new_posts['replyto'] = []
    
    db.posts.update(
        {'_id':new_posts['_id']},
        new_posts
    )
