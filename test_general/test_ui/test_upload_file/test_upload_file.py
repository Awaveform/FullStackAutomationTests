from pathlib import Path

import pytest

TEST_DATA_PATH = Path(__file__).parent / "_test_data"

upload_cases = [
    ("sample_min_size.txt", "upload min size file"),
    ("sample_one_mb_size.txt", "upload max size file"),
    ("sample_empty.txt", "upload empty file"),
    ("simple_image.jpeg", "upload image file"),
    ("undefined_file_format", "upload undefined file"),
    ("файл_äüß.txt", "upload special characters"),
]


@pytest.mark.parametrize(
    "filename",
    [case[0] for case in upload_cases], ids=[case[1] for case in upload_cases]
)
def test_upload_valid_files(upload_page, filename):
    """
    Test uploading different valid file types and assert a success message.
    """
    file_path = TEST_DATA_PATH / filename
    upload_page.open_page_url()
    upload_page.select_file(file_path)
    upload_page.upload_file()
    upload_page.assert_upload_success(filename)


def test_upload_without_file(upload_page):
    """
    Test upload button click without file selection. Expects a validation
    message. Raises an expected exception which is considered as a
    successful test result.
    """
    upload_page.open_page_url()
    upload_page.upload_file()
    upload_page.assert_upload_validation_msg(msg="No file selected")


@pytest.mark.skip(reason="Absent requirements")
def test_upload_invalid_files(upload_page):
    """
    Placeholder for testing invalid file uploads.
    """
    pass


def test_drag_and_drop_file(upload_page):
    """
    Test drag-and-drop upload functionality.
    """
    file_path = TEST_DATA_PATH / "simple_image.jpeg"
    upload_page.open_page_url()
    upload_page.drag_and_drop_file(file_path)
    upload_page.assert_upload_success("simple_image.jpeg")


def test_change_upload_file(upload_page):
    """
    Test changing selected file before upload. Expect a final file to
    be uploaded.
    """
    file_path = TEST_DATA_PATH / "simple_image.jpeg"
    file_path_edited = TEST_DATA_PATH / "sample_min_size.txt"
    upload_page.open_page_url()
    upload_page.select_file(file_path)
    upload_page.select_file(file_path_edited)
    upload_page.upload_file()
    upload_page.assert_upload_success("sample_min_size.txt")
