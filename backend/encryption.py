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

    def register(self, nickname=None, user=None, password=None):
        if user in self.data: # if the user already exists in the database, return False
            return "User already exists"
        if len(password) < 6:
            return "paswword < 6"
        if len(user) == 0:
            return "User empty"
        pwd_hash = self.hash_password(password) # hash the password
        self.data[user] = [nickname, pwd_hash, watchlist] # add the user to the dictionary
        with open('encrypted_dict.json', 'wb') as f: # save the dictionary to the file
            pickle.dump(self.data, f, protocol=pickle.HIGHEST_PROTOCOL) 
        self.user = user
        return self.data[user] # Use successfully registered
        
    def login(self, user, password):
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
        for category in data[self.user][2]:
            for id in data[self.user][2][category]:
                if drama_id == id and value in options:
                    while drama_id in data[self.user][2][category]:
                        data[self.user][2][category].remove(id)

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
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
        return True

    def remove_from_watchlist(self, drama_id):
        with open('encrypted_dict.json', 'rb') as f:
            data = pickle.load(f)
        for category in data[self.user][2]:
            for id in data[self.user][2][category]:
                if drama_id == id:
                    data[self.user][2][category].remove(drama_id)
                    with open('encrypted_dict.json', 'wb') as f: # save the dictionary to the file
                        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
                    return True
        return False
    
    def get_dramas(self):
        with open('encrypted_dict.json', 'rb') as f:
            data = pickle.load(f)
        try:
            user = self.user
            return data[user][2]
        except:
            return False


#{user: [nickname, pass, {currently watching: [],  }}