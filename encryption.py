import bcrypt

# Temporary password
input_password = str(input("Inputer Password: "))
encoded_password = input_password.encode("utf-8") # encode the password
encrypted_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt(10)) # encrypt the password
print(encrypted_password)
