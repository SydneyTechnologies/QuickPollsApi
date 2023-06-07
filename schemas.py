from pydantic import BaseModel
from typing import List

# VOTE SCHEMAS
class BaseVote(BaseModel):
    voterId: str
    pollId: str
    optionId: str
    pass

class CreateVote(BaseVote):
    pass

class Vote(BaseVote):
    id: str
    class Config:
        orm_mode = True


# OPTION SCHEMAS
class BaseOption(BaseModel):
    value: str
    pass

class CreateOption(BaseOption):
    pollId: str
    pass

class Options(BaseModel):
    votes: List[Vote]
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


# POLLS SCHEMA 
class BasePoll(BaseModel):
    question: str
    private: bool
    protected: bool 
    closed: bool 

class CreatePoll(BasePoll):
    pass

class Poll(BasePoll):
    id: str
    owner_id: str
    created_at: str
    options = List[Options]
    votes = List[Vote]
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

# USER SCHEMAS
class BaseUser(BaseModel):
    first_name : str
    last_name: str
    email: str 

class CreateUser(BaseUser):
    password: str

    class Config:
        schema_extra={
            "example":{
            "first_name": "John",
            "last_name":"Doe",
            "email":"JohnDoe@gmail.com",
            "password": "some password"
            }
        }

class User(BaseUser):
    id: str
    polls: List[Poll]
    votes: List[Vote]
    created_at: str
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True




