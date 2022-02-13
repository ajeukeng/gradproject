import pytest
from common_utilities import get_file_from_path


@pytest.fixture()
def test_db_location():
    db_location = get_file_from_path('../docs/test_db.db', __file__)

    return db_location
