from pydantic import BaseModel

class BaseUser(BaseModel):
    # this is the generic class for a user 
    first_name: str
    last_name: str
    email: str


class CreateUser(BaseUser):
    password: str

class UpdateUserPassword(BaseModel):
    password: str | None = None

class UpdateUser(BaseUser):
    pass

class User(BaseUser):
    id: str
    polls: list[str]

class BasePoll(BaseModel):
    question: str
    private: bool = False
    protected: bool = False
    closed: bool = False
    owner_id: str
    options: list[str] = []
    

class CreatePoll(BasePoll):
    pass

class UpdatePoll(BasePoll):
    pass

class BaseVote(BaseModel):
    pass

class CreateVote(BaseVote):
    voterId: str
    pollId: str
    optionId: str