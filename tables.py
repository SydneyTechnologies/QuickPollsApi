from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UUID, DateTime
from sqlalchemy.orm import relationship
from databaseConnection import BaseTable
from datetime import datetime
import uuid


def generateUUID():
    return str(uuid.uuid4())

class User(BaseTable):
    __tablename__ = "Users"

    id = Column(String, unique=True, primary_key=True, nullable=False, default=generateUUID)
    first_name = Column(String, nullable=False, default="Sydney")
    last_name = Column(String, nullable=False, default="Idundun")
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    #relationships
    polls = relationship("Polls", back_populates="owner")
    votes = relationship("Votes", back_populates="voter")

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name
    

class Poll(BaseTable):
    __tablename__ = "Polls"

    id = Column(String, unique=True, primary_key=True, default=generateUUID)
    question = Column(String, nullable=False)
    private = Column(Boolean, nullable=False, default=False)
    protected = Column(Boolean, nullable=False, default=False)
    closed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    # Relationships 
    owner_id = Column(String, ForeignKey("Users.id"))
    owner = relationship("Users", back_populates="polls")


    options = relationship("Options", back_populates="poll")
    votes = relationship("Votes", back_populates="poll")


class Option(BaseTable):
    __tablename__ = "Options"

    id = Column(String, nullable=False, primary_key=True, default=generateUUID)
    value = Column(String, nullable=False)

    #Relationships
    pollId = Column(String, ForeignKey("Polls.id"))
    poll = relationship("Polls", back_populates="options")

    votes = relationship("Votes", back_populates="option")


class Vote(BaseTable):
    __tablename__ = "Votes"

    id = Column(String, primary_key=True, default=generateUUID)

    #Relationships
    voterId = Column(String, ForeignKey("Users.id"))
    voter = relationship("Users", back_populates="votes")

    pollId = Column(String, ForeignKey("Polls.id"))
    poll = relationship("Polls", back_populates="votes")

    optionId = Column(String, ForeignKey("Options.id"))
    option = relationship("Options", back_populates="Options")

