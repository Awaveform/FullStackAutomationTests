import pytest
import requests

from models import Post
from test_general.conftest import validate_response
from utilities.env_settings import env_settings


def test_create_post_valid():
    """
    Test creating a post with valid payload.
    """
    payload = {"title": "foo", "body": "bar", "userId": 1}
    r = requests.post(f"{env_settings.API_BASE}/posts", json=payload)
    assert r.status_code == 201
    data = validate_response(Post, r.json())
    assert data.title == payload["title"]


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"title": "only title"},
        {"userId": "not-an-int"},
        {"title": None, "body": "bar", "userId": 1},
        {"title": "valid", "body": "valid", "userId": -5},
    ],
    ids=[
        "empty_payload",
        "only_title",
        "invalid_userId",
        "null_title",
        "neg_userId"
    ]
)
def test_create_post_invalid_schema(payload):
    """
    Test creating posts with various invalid payloads; expect validation
    to fail.
    """
    r = requests.post(f"{env_settings.API_BASE}/posts", json=payload)
    assert r.status_code == 201
    with pytest.raises(Exception):
        validate_response(Post, r.json(), raise_on_error=False)


def test_invalid_post_shape():
    """
    Test post with structurally invalid shape; expect validation error.
    """
    malformed = {"userId": "not-an-int", "id": 1, "title": "ok", "body": "ok"}
    with pytest.raises(Exception):
        validate_response(Post, malformed, raise_on_error=False)
