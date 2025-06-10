import pytest
import requests

from models import Post, PostList
from test_general.conftest import validate_response
from utilities.env_settings import env_settings


def test_get_all_posts():
    """
    Test retrieving all posts; expect 100 items with valid structure.
    """
    r = requests.get(f"{env_settings.API_BASE}/posts")
    assert r.status_code == 200
    posts = validate_response(PostList, r.json()).root
    assert len(posts) == 100


@pytest.mark.parametrize("post_id", [1, 50, 100],
                         ids=lambda v: f"valid_id_{v}")
def test_get_post_valid(post_id):
    """
    Test retrieving individual post by valid ID.
    """
    r = requests.get(f"{env_settings.API_BASE}/posts/{post_id}")
    assert r.status_code == 200
    post = validate_response(Post, r.json())
    assert post.id == post_id


@pytest.mark.parametrize("post_id", [0, 101, 999],
                         ids=lambda v: f"invalid_id_{v}")
def test_get_post_invalid(post_id):
    """
    Test retrieving individual post by invalid ID; expect 404 and empty
    response.
    """
    r = requests.get(f"{env_settings.API_BASE}/posts/{post_id}")
    assert r.status_code == 404
    assert r.text == '{}'


def test_response_headers():
    """
    Test that API response has the correct JSON content-type header.
    """
    r = requests.get(f"{env_settings.API_BASE}/posts")
    assert r.headers.get("Content-Type", "").startswith("application/json")


def test_duplicate_post_ids():
    """
    Test that all posts have unique IDs.
    """
    r = requests.get(f"{env_settings.API_BASE}/posts")
    posts = validate_response(PostList, r.json()).root
    ids = [p.id for p in posts]
    assert len(ids) == len(set(ids))


def test_get_posts_with_params_ignored():
    """
    Test that query params are ignored when retrieving all posts.
    """
    r = requests.get(f"{env_settings.API_BASE}/posts", params={"userId": 1})
    assert r.status_code == 200
    validate_response(PostList, r.json())


@pytest.mark.parametrize("user_id", [-1, -99], ids=lambda v: f"neg_user_{v}")
def test_get_posts_invalid_user_id(user_id):
    """
    Test behavior when using invalid userId query param.
    """
    r = requests.get(f"{env_settings.API_BASE}/posts",
                     params={"userId": user_id})
    assert r.status_code in (200, 400, 404)
    try:
        data = r.json()
        assert isinstance(data, list)
    except ValueError:
        pytest.fail("Response not JSON")
