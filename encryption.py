import bcrypt

# Temporary password
input_password = str(input("Inputer Password: "))
encoded_password = input_password.encode("utf-8") # encode the password
encrypted_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt(10)) # encrypt the password

check_password = str(input("check password: ")) # input the password to check
encoded_check_password = check_password.encode("utf-8") # encode the password

if bcrypt.checkpw(encoded_check_password, encrypted_password):
    print("login success")
else:
    print("incorrect password")