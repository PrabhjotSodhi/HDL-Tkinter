import pickle
import bcrypt

watchlist = {
    "plan_to_watch":[
    ],
    "currently_watching":[
    ],
    "completed":[
    ],
    "on_hold":[
    ],
}

class PasswordDatabase:
    def __init__(self):
        try:
            with open('encrypted_dict.json', 'rb') as f:
                self.data = pickle.load(f)
        except: # if file does not exist or is empty, create new dictionary
            self.data = {}

    def register(self, nickname, user, password):
        if user in self.data: # if the user already exists in the database, return False
            return False
        pwd_hash = self.hash_password(password) # hash the password
        self.data[user] = [nickname, pwd_hash, watchlist] # add the user to the dictionary
        with open('encrypted_dict.json', 'wb') as f: # save the dictionary to the file
            pickle.dump(self.data, f, protocol=pickle.HIGHEST_PROTOCOL) 
        return True # Use successfully registered
        
    def login(self, user, password):
        if user not in self.data: # if the user does not exist in the database, return False
            return False
        pwd_bytes = password.encode('utf-8')
        if bcrypt.checkpw(pwd_bytes, self.data[user][1]): # if the password is correct, return True
            return self.data[user]
        else:
            return False

    def hash_password(self, password):
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt() # generate a salt that is used to hash the password
        return bcrypt.hashpw(pwd_bytes, salt)


'''
db = PasswordDatabase()

# Test the system
print("-------------Registering users-------------")
print(db.register('john','john', '123'))
print(db.register('john','john', '123'))
print(db.register('john','jeff', '345'))
print(db.register('john','joe', '456'))

print("-------------Login-------------")
print(db.login('john', '123'))
print(db.login('john', '345'))
print(db.login('joe', '678'))
'''


#{user: [nickname, pass, {currently watching: [],  }}