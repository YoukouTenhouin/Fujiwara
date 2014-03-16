from hashlib import sha256
from base64 import b64decode,b64encode

from bson.objectid import ObjectId

class Auth:
    def __init__(self,key):
        self.key = key
        self.hashed_key = sha256(key.encode()).hexdigest()

    def getSign(self,string):
        try:
            string = string.encode()
        except:
            pass

        hashed_str = sha256(string).hexdigest()

        xor_result = b''
        
        for i in range(len(hashed_str)):
            a = ord(hashed_str[i])
            b = ord(self.hashed_key[i])
            xor_result += bytes(a^b)
            
        return sha256(xor_result).hexdigest()
        
    def vaild(self,str):
        try:
            data,sign = str.split('|')
        except:
            return False
        
        return (sign == self.getSign(data))

    def decodeData(self,data):
        b64data,_ = data.split('|')
        uid = b64decode(b64data).decode()
        uid = ObjectId(uid)
        return {"uid":uid}
        
    def encodeData(self,user):
        uid = str(user["uid"])
        
        data = b64encode(uid.encode())

        sign = self.getSign(data)
        return '|'.join([data.decode(),sign])
