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
    "dropped":[
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
            print("nidnaidniwand")
            return "User already exists"
        if len(password) < 6:
            return "paswword < 6"
        pwd_hash = self.hash_password(password) # hash the password
        self.data[user] = [nickname, pwd_hash, watchlist] # add the user to the dictionary
        with open('encrypted_dict.json', 'wb') as f: # save the dictionary to the file
            pickle.dump(self.data, f, protocol=pickle.HIGHEST_PROTOCOL) 
        self.user = user
        return self.data[user] # Use successfully registered
        
    def login(self, user, password):
        #print(self.data)
        if user not in self.data: # if the user does not exist in the database, return False
            return "User does not exist"
        pwd_bytes = password.encode('utf-8')
        if bcrypt.checkpw(pwd_bytes, self.data[user][1]): # if the password is correct, return True
            self.user = user
            return self.data[user]
        else:
            return False

    def hash_password(self, password):
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt() # generate a salt that is used to hash the password
        return bcrypt.hashpw(pwd_bytes, salt)
    
    def add_to_watchlist(self, value, drama_id):
        with open('encrypted_dict.json', 'rb') as f: # save the dictionary to the file
            data = pickle.load(f)
        
        options = ["Plan to watch","Currently watching","Completed","On hold","Dropped"]
        print(data[self.user][2])
        for category in data[self.user][2]:
            for id in data[self.user][2][category]:
                if drama_id == id and value in options:
                    while drama_id in data[self.user][2][category]:
                        data[self.user][2][category].remove(id)
        print(data[self.user][2])

        if value == "Select an option":
            return False
        elif value == "Plan to watch":
            data[self.user][2]["plan_to_watch"].append(drama_id) # add the title to the plan to watch list
        elif value == "Currently watching":
            data[self.user][2]["currently_watching"].append(drama_id)
        elif value == "Completed":
            data[self.user][2]["completed"].append(drama_id)
        elif value == "On hold":
            data[self.user][2]["on_hold"].append(drama_id)
        elif value == "Dropped":
            data[self.user][2]["dropped"].append(drama_id)
        else:
            return False
        with open('encrypted_dict.json', 'wb') as f: # save the dictionary to the file
            print(data[self.user])
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


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