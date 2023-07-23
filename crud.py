from databaseConnection import localSession
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import update
import tables
import schemas


def get_user( email:str, db: Session, )->tables.User:
    user = db.query(tables.User).filter(tables.User.email == email).first()
    return user

def get_user_byId(userId:str, db: Session)->tables.User:
    user = db.query(tables.User).filter(tables.User.id == userId).first()
    return user

def get_poll(pollId:str, db: Session)->tables.Poll:
    poll = db.query(tables.Poll).filter(tables.Poll.id == pollId).first()
    return poll

def get_option(optionId:str, db: Session)->tables.Option:
    option = db.query(tables.Option).filter(tables.Option.id == optionId).first()
    return option

def get_vote(voteId:str, db: Session)->tables.Vote:
    vote = db.query(tables.Vote).filter(tables.Vote.id == voteId).first()
    return vote

def update_user(user: tables.User, userData: schemas.UpdateUser, db: Session):
    # first remove non values 
    updates = {}
    for key, value in userData.dict().items():
        if value != None:
            updates[key] = value
    if user: 
        update_query = update(tables.User).where(tables.User.email == user.email).values(updates)
        db.execute(update_query)
        db.commit()
        db.refresh(user)
    return user

def update_poll(poll: tables.Poll, pollData: schemas.UpdateUser, db: Session):
    # first remove non values 
    updates = {}
    for key, value in pollData.dict().items():
        if value != None:
            updates[key] = value

    update_query = update(tables.Poll).where(tables.Poll.id == poll.id).values(updates)
    db.execute(update_query)
    db.commit()
    db.refresh(poll)
    return poll


def delete_from_db(dbObject: any, db: Session )-> bool:
    if dbObject:
        db.delete(dbObject)
        db.commit()
        return True
    
    return False
                
def add_user(user: tables.User, db:Session):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
    

def add_to_db(dbObject: any, db: Session)->tables.BaseTable:
    if dbObject:
        db.add(dbObject)
        db.commit()
        db.refresh(dbObject)
    return dbObject



def get_db_objects(object: tables.BaseTable, db: Session)->list[tables.BaseTable]:
    results = db.query(object).all()
    return results