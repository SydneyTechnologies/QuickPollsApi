from fastapi import FastAPI, Depends, HTTPException, status
import tables, crud, schemas
from databaseConnection import engine
from utils import *

tables.BaseTable.metadata.create_all(bind=engine)
DESCRIPTION = "The QuickPolls API is a powerful and interactive platform built with FastAPI that allows users to create and participate in polls, while providing real-time live voting statistics. 🗳️📊"
app = FastAPI(title="QuickPollsApi", description=DESCRIPTION)


#setting up a simple server with fastAPI
@app.post("/register/", tags=["User"], description="This endpoint is responsible for taking in user data encrypting the password and storing the user in the database")
def createUser(userData: schemas.CreateUser, db = Depends(get_db)):
    if crud.get_user(userData.email, db=db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User exists")
    
    hashed_password = hashPassword(userData.password)
    userData.password = hashed_password
    new_user = tables.User(**userData.dict())
    new_user = crud.add_to_db(new_user, db=db)
    return schemas.User.from_orm(new_user)

# @app.post("/login", description="Log user to quickPolls Application")
# def login(loginData: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), db = Depends(get_db)):
#     user = crud.get_user(loginData.username, db=db)
#     if user: 
#         if validatePassword(loginData.password, user.password):
#             token = generateAccessToken(user.email)
#             return {"access_token": token, "token_type": "bearer"} 
#         else:
#             return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Password")

#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# @app.get("/users")
# def getAllUsers(db = Depends(get_db)):
#     users: list[tables.User] = crud.get_db_objects(object=tables.User, db=db)
#     results = [schemas.User.from_orm(user) for user in users]
#     return results

# @app.delete("/users")
# def deleteUser(email: str, db = Depends(get_db)):
#     user = crud.get_user(email=email, db=db)
#     result = crud.delete_from_db(user, db=db)
#     if result: 
#         return user
#     else: 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


# @app.post("/polls")
# def createPoll(pollData: schemas.CreatePoll, user: tables.User = Depends(get_current_user), db = Depends(get_db)):
#     poll = pollData.copy()
#     poll = poll.dict()
#     poll.update({"owner_id": user.id})
#     new_poll = tables.Poll(**poll)
#     new_poll = crud.add_to_db(new_poll, db)
#     if new_poll:
#         return schemas.Poll.from_orm(new_poll)

# @app.get("/polls")
# def listPolls(db = Depends(get_db)):
#     polls: list[tables.Poll] | None = crud.get_db_objects(object=tables.Poll, db=db)
#     if polls :
#         for p in polls: 
#             print(schemas.Poll.from_orm(p))
#         return [ schemas.Poll.from_orm(poll) for poll in polls]
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

