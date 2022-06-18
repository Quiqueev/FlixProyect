import os
import csv
from sqlalchemy import (
    MetaData,
    Column,
    Integer,
    String,
    Float,
    TIMESTAMP,
    Text,
    create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from abc import ABC, abstractmethod
from manage import users

def get_postgres_uri():
    host = os.environ.get("DB_HOST", "postgres")
    port = 5432
    password = os.environ.get("DB_PASS", "abc123")
    user, db_name = "movies", "movies"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


Base = declarative_base(
    metadata=MetaData(),
)


engine = create_engine(
    get_postgres_uri(),
    isolation_level="REPEATABLE READ",
)


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    preference_key = Column(Integer)
    movie_title = Column(String)
    rating = Column(Float)
    year = Column(Integer)
    create_time = Column(TIMESTAMP(timezone=True), index=True)

# FILM
# SOLID 1 --> SRP: only takes care of films
class Film:
    def __init__(self, list):
        self.title = list[1]
        self.key = list[0]
        self.rating = list[3]
        self.star_cast = list[2]
        self.year = list[4]
    
    def write(self):
        print(f'Title: {self.title}, key: {self.preference_key}')
    
    def jsonify(self):
        return {
            'key': self.key,
            'title': self.title,
            'rating': self.rating,
            'year': self.year,
            'cast': self.star_cast
        }

# USER
# CHAIN OF RESPONSABILITY
class UserHandler(object):
    def __init__(self, nxt):
        self._nxt = nxt
 
    def handle(self, request):
        handled = self.processRequest(request)
        return handled
 
        if not handled:
            self._nxt.handle(request)
 
    def processRequest(self, request):
        raise NotImplementedError('Needs to be implemented')
 
 
class FirstUserAuth(UserHandler): 
    def processRequest(self, request):
        if (request in users):
            return True
        else:
            return False

class User:
    def __init__(self, user):
        self.user = user
        value = FirstUserAuth(None)
        self.exists = value.handle(user)
    

    def create_list(self, list_type):

        if (self.exists):
            # SIMPLE FACTORY
            if (list_type == 'film'):
                return MovieList()
            else:
                return None

        else:
            return 400

# SOLID 2 --> OCP: Can add methods to Movie list or other lists that could be later created like (Series Recommendation list)
class Rlist(ABC):
    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def getList(self):
        pass

    @abstractmethod
    def getSize(self):
        pass

# SOLID 3 --> ISP: Some future list classes may not need to read from a CSV list. 
class Reader(ABC):
    @abstractmethod
    def readCSV(self, size, calc):
        pass

class MovieList(Rlist, Reader):
    def __init__(self):
        self.movie_list = []
    
    # Add item to list
    def add(self, film_row):
        film = Film(film_row) # Create obj Film 
        self.movie_list.append(film.jsonify())
    
     # Return list
    def getList(self):
        return self.movie_list
    
     # Return list size
    def getSize(self):
        return len(self.movie_list)
    
    def readCSV(self, size, calc):
        with open("recommendation_results.csv", "r", newline="") as file:
            csvreader = csv.reader(file)
            headers = next(csvreader)

            for row in csvreader:
                if(len(self.movie_list) == size): break
                if (int(row[0]) == calc):
                    film = Film(row) # Create obj Film 
                    self.movie_list.append(film.jsonify())

def start_mappers():
    Base.metadata.create_all(engine)