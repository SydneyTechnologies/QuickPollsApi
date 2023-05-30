from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///.sql_app.db"
# this is the database we will be connecting to 

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# we connect to our local sql database that is hosted on the server and tell sql not to
# check if it is the same thread that is communication with the database
localSession = sessionmaker(autoCommit=False, autoflush=False, bind=engine)
# this is the point of connection to the database it is an instance of the database 
BaseTable = declarative_base()
# the base class that allows for creating tables in a database 