import pytest
from app import create_app

@pytest.fixture
def client():
    test_db_location = 'sqlite:///test-merchant.db'

    app = create_app(test_db_location)
    app.config['TESTING'] = True

    with app.app_context():
        client = app.test_client()
        yield client   