from fastapi import FastAPI, Depends, HTTPException, status
import tables, crud, schemas
from databaseConnection import engine
from utils import *
from endpoints import user, polls, options

tables.BaseTable.metadata.create_all(bind=engine)
DESCRIPTION = "The QuickPolls API is a powerful and interactive platform built with FastAPI that allows users to create and participate in polls, while providing real-time live voting statistics. 🗳️📊"
app = FastAPI(title="QuickPollsApi", description=DESCRIPTION)

app.include_router(user.router)
app.include_router(polls.router)
app.include_router(options.router)



