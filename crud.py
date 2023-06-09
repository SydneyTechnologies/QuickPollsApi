from databaseConnection import localSession
from fastapi import Depends
from sqlalchemy.orm import Session
import tables
import schemas


def get_user(email:str, db: Session):
    user = db.query(tables.User).filter(tables.User.email == email).first()
    return user

def delete_from_db(dbObject: any, db: Session ):
    if dbObject:
        db.delete(dbObject)
        db.commit()
        return True
    
    return False
                

def add_to_db(dbObject: any, db: Session):
    if dbObject:
        db.add(dbObject)
        db.commit()
        db.refresh(dbObject)
    return dbObject



def get_db_objects(object: tables.BaseTable,  db: Session):
    results = db.query(object).all()
    return results