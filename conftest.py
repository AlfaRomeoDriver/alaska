import pytest

from api.client import Bear

@pytest.fixture(scope="session", autouse=True)
def test_session(request):
    yield Bear("http://127.0.0.1:9091")

@pytest.fixture(scope="module")
def bear_client(test_session):
    yield test_session

@pytest.fixture(scope="session", autouse=True)
def clean_up_session(test_session):
    yield
    # Говорит что все действия в сессии завершены
    test_session.clean_up()

