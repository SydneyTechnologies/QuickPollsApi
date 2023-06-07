import bcrypt
def hashPassword(password: str):
    encoded_password = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hashed_password


def validatePassword(entry: str, password: str):
    encoded_entry = entry.encode("utf-8")
    if bcrypt.checkpw(encoded_entry, password):
        return True
    else:
        return False
