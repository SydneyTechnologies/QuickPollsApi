from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
import schemas, crud, utils, tables

router = APIRouter()

@router.post("/polls", tags=["Poll"], summary="Create a poll for this user")
def createPoll(pollData: schemas.CreatePoll, user: tables.User = Depends(utils.get_current_user), db = Depends(utils.get_db)):
    poll = pollData.copy()
    poll = poll.dict()
    poll.update({"owner_id": user.id})
    print(poll)
    new_poll = tables.Poll(**poll)
    new_poll = crud.add_to_db(new_poll, db)
    if new_poll:
        return schemas.Poll.from_orm(new_poll)
    
@router.put("/polls/{pollId}", tags=["Poll"], summary="Update poll by pollId")
def updatePoll(pollId:str, pollData : schemas.UpdatePoll, user = Depends(utils.get_current_user), db = Depends(utils.get_db)):
    poll: tables.Poll = crud.get_poll(pollId, db)
    if poll: 
        if poll.owner != user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You don't own this poll")
        


    return "Hi"


@router.delete("/polls/{pollId}", tags=["Poll"], summary="Delete poll by pollId")
def deletePoll(pollId:str):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@router.get("/polls",  tags=["Poll"], summary="List all the polls in the database")
def listPolls(db = Depends(utils.get_db)):
    polls: list[tables.Poll] | None = crud.get_db_objects(object=tables.Poll, db=db)
    if polls :
        return [ schemas.Poll.from_orm(poll) for poll in polls]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)