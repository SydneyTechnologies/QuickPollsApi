from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
import schemas, crud, utils, tables

router = APIRouter()

@router.get("/polls/search", tags=["Poll"], summary="Search polls by question")
def searchPolls(question:str = None, db= Depends(utils.get_db)):
    query = db.query(tables.Poll)

    # Apply filters based on the provided query parameters
    if question:
        query = query.filter(tables.Poll.question.ilike(f"%{question}%"))

    # if author:
    #     query = query.filter(tables.Poll.author.ilike(f"%{author}%"))

    # Execute the query and return the results
    results = query.all()
    return results

@router.post("/polls", tags=["Poll"], summary="Create a poll for this user")
def createPoll(pollData: schemas.CreatePoll, user: tables.User = Depends(utils.get_current_user), db = Depends(utils.get_db)):
    poll = pollData.copy()
    poll = poll.dict()
    poll.update({"owner_id": user.id})
    options_list = poll.pop("options")
    new_poll = tables.Poll(**poll)
    new_poll: tables.Poll = crud.add_to_db(new_poll, db)
    if new_poll:
        if options_list: 
            for option in options_list: 
                print(option)
                new_option = schemas.CreateOption(value=option, pollId=new_poll.id)
                crud.add_to_db(tables.Option(**new_option.dict()), db)

        return schemas.Poll.from_orm(new_poll)
    
@router.put("/polls/{pollId}", tags=["Poll"], summary="Update poll by pollId")
def updatePoll(pollId:str, pollData : schemas.UpdatePoll, user = Depends(utils.get_current_user), db = Depends(utils.get_db)):
    poll: tables.Poll = crud.get_poll(pollId, db)
    if poll: 
        if poll.owner != user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You don't own this poll")
        updatedPoll = crud.update_poll(poll, pollData, db)
    return schemas.Poll.from_orm(updatedPoll)


@router.delete("/polls/{pollId}", tags=["Poll"], summary="Delete poll by pollId")
def deletePoll(pollId:str, db = Depends(utils.get_db)):
    poll = crud.get_poll(pollId=pollId, db=db)
    if poll: 
        result = crud.delete_from_db(poll,db=db)
        return result
    else:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")

@router.get("/polls",  tags=["Poll"], summary="List all the polls in the database")
def listPolls(db = Depends(utils.get_db)):
    polls: list[tables.Poll] | None = crud.get_db_objects(object=tables.Poll, db=db)
    if polls :
        return [ schemas.Poll.from_orm(poll) for poll in polls]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    


@router.get("/polls/{id}", tags=["Poll"], summary="View specific poll data")
def getPoll(id:str, db = Depends(utils.get_db), user: tables.User = Depends(utils.get_current_user)):
    poll = crud.get_poll(id, db)
    if poll: 
        return schemas.Poll.from_orm(poll)

        # if user.id == poll.owner_id:
        #     return schemas.Poll.from_orm(poll)
        # else:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
