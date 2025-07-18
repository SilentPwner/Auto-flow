import pytest
from app import create_app, db
from app.core.config import TestConfig

@pytest.fixture(scope='module')
def test_app():
    """Create and configure a new app instance for each test module."""
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app # هذا هو ما سيستخدمه الاختبار
        db.drop_all()

@pytest.fixture(scope='module')
def test_client(test_app):
    """A test client for the app."""
    return test_app.test_client()