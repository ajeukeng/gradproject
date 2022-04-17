import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common_utilities import get_file_from_path


@pytest.fixture()
def test_db_location():
    db_location = get_file_from_path('docs/test_only_db.db', __file__)
    return db_location


@pytest.fixture
def test_session():
    db_location = get_file_from_path('docs/test_db.db', __file__)
    print(db_location)
    engine = create_engine(f'sqlite:///{db_location}', echo=True)
    Session = sessionmaker(bind=engine)
    # create a new session
    session = Session()

    return session