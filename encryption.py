import pickle
import bcrypt

class PasswordDatabase:
    def __init__(self):
        try:
            with open('encrypted_dict.json', 'rb') as f:
                self.data = pickle.load(f)
        except:
            self.data = {}
    def register(self, user, password):
        if user in self.data:
            return False
        pwd_hash = self.hash_password(password)
        self.data[user] = pwd_hash
        with open('encrypted_dict.json', 'wb') as f:
            pickle.dump(self.data, f, protocol=pickle.HIGHEST_PROTOCOL)
        return True

db = PasswordDatabase()

print("-------------Registering users-------------")
print(db.register('john', '123'))
print(db.register('john', '123'))
print(db.register('jeff', '345'))
print(db.register('joe', '456'))
