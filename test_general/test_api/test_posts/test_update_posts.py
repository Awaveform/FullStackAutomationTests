import pytest
import requests

from models import Post
from test_general.conftest import validate_response
from utilities.env_settings import env_settings


@pytest.mark.parametrize("method", ["put", "patch"],
                         ids=lambda m: f"method_{m}")
def test_update_post_valid(method):
    """
    Test updating a post with valid payload using PUT and PATCH.
    """
    payload = {"title": "update", "body": "update", "userId": 1}
    url = f"{env_settings.API_BASE}/posts/1"
    r = getattr(requests, method)(url, json=payload)
    assert r.status_code == 200
    data = validate_response(Post, r.json())
    assert data.title == payload["title"]


@pytest.mark.parametrize("method", ["put", "patch"],
                         ids=lambda m: f"method_{m}")
@pytest.mark.parametrize(
    "payload",
    [
        {"userId": "bad"},
        {"title": None, "body": "x", "userId": 1},
        {"title": "x", "body": None, "userId": 1},
        {"title": "x", "body": "y", "userId": -10},
        {"title": 123, "body": "y", "userId": 1},
        {"title": "x", "body": 456, "userId": 1},
    ],
    ids=[
        "bad_userId",
        "null_title",
        "null_body",
        "neg_userId",
        "int_title",
        "int_body"
    ]
)
def test_update_post_invalid_schema(method, payload):
    """
    Test updating a post with invalid payloads; expect schema
    validation to fail.
    """
    url = f"{env_settings.API_BASE}/posts/1"
    r = getattr(requests, method)(url, json=payload)
    assert r.status_code == 200
    with pytest.raises(Exception):
        validate_response(Post, r.json(), raise_on_error=False)
