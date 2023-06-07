from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import tables
from databaseConnection import localSession, engine
import schemas
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
def createUser(userData: schemas.CreateUser, db: Session = Depends(get_db)):
    if db.query(tables.User).filter(tables.User.email == userData.email).first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User exists")
    
    hashed_password = hashPassword(userData.password)
    userData.password = hashed_password
    new_user = tables.User(**userData.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users")
def getAllUsers(db: Session = Depends(get_db)):
    users = db.query(tables.User).all()
    results = [schemas.User.from_orm(user) for user in users]
    return results

@app.delete("/users")
def deleteUser(email: str | None = None, id:str|None = None, db: Session = Depends(get_db)):
    if email: 
        user = db.query(tables.User).filter(tables.User.email == email)
    elif id: 
        user = db.get(tables.User, id)
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user