import bcrypt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt;
from databaseConnection import localSession
import binascii
import crud


auth_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "b5b8ab37b82485ae5acdc59a59e69aab00fdf22dcc6232d6fb86e63f18e29194"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

# dependency 
def get_db():
    db = localSession()
    try: 
        yield db
    finally: 
        db.close()

def hashPassword(password: str):
    print("Hashing password")
    print(f"password given is: {password}")
    encoded_password = password.encode("utf-8")
    print(f"byte password is: {encoded_password}")
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    print(f"hashed password given is: {hashed_password}")
    return hashed_password


def validatePassword(entry: str, password: str):
    password = binascii.unhexlify(password[2:])
    encoded_entry = entry.encode("utf-8")

    if bcrypt.checkpw(encoded_entry, password):
        return True
    else:
        return False
    
def generateAccessToken(email: str):
    expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    tokenData = {"email":email, "expiration": expiration_time.isoformat()}
    encoded_jwt = jwt.encode(tokenData, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token:str = Depends(auth_scheme), db = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        print(payload)
        if email is None:
            raise credentials_exception
    except JWTError:
        # email: str = payload.get("email")
        print(token)
        raise credentials_exception
    user = crud.get_user(email=email, db=db)
    if user is None:
        raise credentials_exception
    return user