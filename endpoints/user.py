from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
import schemas, crud, utils, tables

router = APIRouter()

@router.post("/register/", tags=["User"], summary="Register a new user")
def register(userData: schemas.CreateUser, db = Depends(utils.get_db)):
    if crud.get_user(userData.email, db=db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User exists")
    
    hashed_password = utils.hashPassword(userData.password)
    userData.password = hashed_password
    new_user = tables.User(**userData.dict())
    new_user = crud.add_to_db(new_user, db=db)
    return schemas.User.from_orm(new_user)

@router.post("/login", tags=["User"], summary="Log user to quickPolls Application")
def login(loginData: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), db = Depends(utils.get_db)):
    user = crud.get_user(loginData.username, db=db)
    if user: 
        if utils.validatePassword(loginData.password, user.password):
            token = utils.generateAccessToken(user.email)
            return {"access_token": token, "token_type": "bearer"} 
        else:
            return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Password")

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/users", tags=["User"], summary="Update general User Information")
def updateUserInfo():
    return "Update User Information"

@router.get("/users", tags=["User"], summary="List all the users in the database")
def listUsers(db = Depends(utils.get_db)):
    users: list[tables.User] = crud.get_db_objects(object=tables.User, db=db)
    if users: 
        results = [schemas.User.from_orm(user) for user in users]
        return results
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.delete("/users", tags=["User"], summary="Delete a specific user by email")
def deleteUser(email: str, db = Depends(utils.get_db)):
    user = crud.get_user(email=email, db=db)
    if user: 
        result = crud.delete_from_db(user, db=db)
        if result: 
            return {"status":f"User {user.email} has successfully been deleted"}
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
