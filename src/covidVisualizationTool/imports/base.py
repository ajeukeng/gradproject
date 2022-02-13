from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class dbBase:
    def __init__(self, db_location):
        self.db_location = db_location
        self.engine = create_engine(f'sqlite:///{db_location}', echo=True)
        Session = sessionmaker(bind=self.engine)
        # create a new session
        self.session = Session()