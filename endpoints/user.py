from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
import schemas, crud, utils, tables

router = APIRouter()


@router.get("/me", tags=["User"], summary="Get current user details")
def currentUser(user = Depends(utils.get_current_user)):
    return user

@router.get("/user/{userId}", tags=["User"], summary="Get current user by Id")
def getUser(userId: str, db = Depends(utils.get_db)):
    user = crud.get_user_byId(userId=userId, db=db)
    return user

@router.post("/register/", tags=["User"], summary="Register a new user")
def register(userData: schemas.CreateUser, db = Depends(utils.get_db)):
    if crud.get_user(userData.email, db=db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User exists")
    
    hashed_password = utils.hashPassword(userData.password)
    userData.password = hashed_password
    print(f"newly hashed password: {userData.password}")

    new_user = tables.User(**userData.dict())
    print(new_user.password)
    new_user = crud.add_user(new_user, db=db)
    print(new_user.password)
    return schemas.User.from_orm(new_user)

@router.post("/login", tags=["User"], summary="Log user to quickPolls Application")
def login(loginData: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), db = Depends(utils.get_db)):
    print(loginData.username, loginData.password)
    user = crud.get_user(loginData.username, db=db)
    if user: 
        if utils.validatePassword(loginData.password, user.password):
            token = utils.generateAccessToken(user.email)
            return {"access_token": token, "token_type": "bearer"} 
        else:
            return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Password")

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/users", tags=["User"], summary="Update general user Information")
def updateUserInfo(userInfo: schemas.UpdateUser, db = Depends(utils.get_db), user = Depends(utils.get_current_user)):
    userInfo.validate()
    updatedUser = crud.update_user(user=user, userInfo=userInfo, db=db)

    if updatedUser: 
        return updatedUser

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@router.get("/users", tags=["User"], summary="List all the users in the database")
def listUsers(db = Depends(utils.get_db)):
    users: list[tables.User] = crud.get_db_objects(object=tables.User, db=db)
    if users: 
        results = [schemas.User.from_orm(user) for user in users]
        return results
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.delete("/users/{email}", tags=["User"], summary="Delete a specific user by email")
def deleteUser(email: str, db = Depends(utils.get_db)):
    user = crud.get_user(email=email, db=db)
    if user: 
        result = crud.delete_from_db(user, db=db)
        if result: 
            return {"status":f"User {user.email} has successfully been deleted"}
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
