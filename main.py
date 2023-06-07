from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import tables
from databaseConnection import localSession, engine
from schemas import CreateUser
from utils import hashPassword

tables.BaseTable.metadata.create_all(bind=engine)

app = FastAPI()

# dependency 
def get_db():
    db = localSession()
    try: 
        yield db
    finally: 
        db.close()

#setting up a simple server with fastAPI
@app.post("/register/", description="This endpoint is responsible for taking in user data encrypting the password and storing the user in the database")
def createUser(userData: CreateUser, db: Session = Depends(get_db)):
    hashed_password = hashPassword(userData.password)
    userData.password = hashed_password
    return userData