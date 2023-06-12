from fastapi import APIRouter, Depends, HTTPException, status
import schemas, utils, crud, tables

router = APIRouter()

@router.post("/options/{pollId}", tags=["Option"], summary="Create a new option for a poll")
def createOption(pollId: str, optionData: schemas.BaseOption, db = Depends(utils.get_db)):
    newOption: tables.Option = tables.Option({**optionData.dict(), "pollId" : pollId})
    newOption = crud.add_to_db(newOption, db)
    if newOption:
        return schemas.Options.from_orm(newOption)
    raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Option creation Failed")


@router.delete("/options/{optionId}", tags=["Option"], summary="Delete an option from a poll")
def deleteOption(optionId: str, db = Depends(utils.get_db)):
    option = crud.get_option(optionId=optionId, db=db)
    result = crud.delete_from_db(dbObject=option, db=db)
    if result: 
        return {"status": f"The option {optionId} has successfully been deleted"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delete operation failed")


@router.get("/options/{optionId}", tags=["Option"], summary="View specific option")
def viewOption(optionId: str, db = Depends(utils.get_db)):
    option = crud.get_option(optionId=optionId, db=db)
    if option: 
        return schemas.Options.from_orm(option)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)