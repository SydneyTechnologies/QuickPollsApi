from fastapi import FastAPI, Depends, HTTPException, status
import tables, crud, schemas
from databaseConnection import engine
from utils import *
from endpoints import user

tables.BaseTable.metadata.create_all(bind=engine)
DESCRIPTION = "The QuickPolls API is a powerful and interactive platform built with FastAPI that allows users to create and participate in polls, while providing real-time live voting statistics. 🗳️📊"
app = FastAPI(title="QuickPollsApi", description=DESCRIPTION)

app.include_router(user.router)

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

