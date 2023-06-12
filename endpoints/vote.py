from fastapi import APIRouter, HTTPException, status, Depends
import schemas, crud, utils, tables

router = APIRouter()

@router.post("/votes/{optionId}", tags=["Vote"], summary="Vote for a specific option")
def Vote(optionId: str, user: tables.User = Depends(utils.get_current_user), db = Depends(utils.get_db)):
    associated_option: tables.Option = crud.get_option(optionId=optionId, db=db)
    if associated_option: 
        new_vote = schemas.CreateVote(voterId=user.id, pollId=associated_option.pollId, optionId=associated_option.id)
        vote = tables.Vote(**new_vote.dict())
        result = crud.add_to_db(dbObject=vote, db=db)
        if result: 
            return schemas.Vote.from_orm(result)
        else: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not add vote")
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="option not found")

@router.delete("/votes/{voteId}", tags=["Vote"], summary="Delete a specific vote")
def DeleteVote(voteId: str, user: tables.User = Depends(utils.get_current_user), db = Depends(utils.get_db)):
    vote = crud.get_vote(voteId=voteId, db=db)
    if vote: 
        result = crud.delete_from_db(dbObject=vote, db=db)
        return {"status": f"vote {vote.id} has been successfully deleted"}
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
