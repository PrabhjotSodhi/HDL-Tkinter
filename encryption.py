import pickle
import bcrypt

class PasswordDatabase:
    def __init__(self):
        try:
            with open('encrypted_dict.json', 'rb') as f:
                self.data = pickle.load(f)
        except:
            self.data = {}
db = PasswordDatabase()