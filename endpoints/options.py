from fastapi import APIRouter, Depends, HTTPException, status
import schemas, utils, crud, tables

router = APIRouter()

@router.post("/options", tags=["Option"], summary="Create a new option for a poll")
def createOption(optionData: schemas.CreateOption, db = Depends(utils.get_db)):
    newOption: tables.Option = tables.Option(**optionData.dict())
    newOption = crud.add_to_db(newOption, db)
    if newOption:
        return schemas.Options.from_orm(newOption)
    raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Option creation Failed")
