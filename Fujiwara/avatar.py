import hashlib

def avatar(user):
    email = user['email'].strip().lower().encode()
    return 'http://www.gravatar.com/avatar/' + hashlib.md5(email).hexdigest()
