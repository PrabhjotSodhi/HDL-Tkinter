import bcrypt


def sign_up(username, password):
    append_string = username.join(password)
    encoded_password = append_string.encode("utf-8") # encode the password
    encrypted_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt(10)) # encrypt the password
    return encrypted_password

def login(username, password):
    append_string = username.join(password)
    encoded_check_password = append_string.encode("utf-8") # encode the password
    if bcrypt.checkpw(encoded_check_password, encrypted_password):
        print("login success")
    else:
        print("incorrect password")

if __name__ == "__main__":
    input_username = str(input("Input Username: "))
    input_password = str(input("Input Password: "))
    check_username = str(input("Check Username: ")) # input the password to check
    check_password = str(input("Check Password: ")) # input the password to check
    encrypted_password = sign_up(input_username, input_password) # encrypt the password
    login(check_username, check_password) # login the password