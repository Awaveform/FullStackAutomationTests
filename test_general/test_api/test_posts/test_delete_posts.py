import pytest
import requests

from utilities.env_settings import env_settings


@pytest.mark.parametrize("post_id", [1, 50, 100], ids=lambda v: f"valid_{v}")
def test_delete_post_valid(post_id):
    """
    Test deleting posts with valid IDs; expect 200 and empty JSON.
    """
    r = requests.delete(f"{env_settings.API_BASE}/posts/{post_id}")
    assert r.status_code == 200
    assert r.json() == {}


@pytest.mark.parametrize("post_id", [0, 9999, -10],
                         ids=lambda v: f"invalid_{v}")
def test_delete_post_invalid(post_id):
    """
    Test deleting posts with invalid IDs; expect 200 and empty JSON.
    """
    r = requests.delete(f"{env_settings.API_BASE}/posts/{post_id}")
    assert r.status_code == 200
    assert r.json() == {}
