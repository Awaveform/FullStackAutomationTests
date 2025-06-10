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
    file_path = TEST_DATA_PATH / filename
    upload_page.open_page_url()
    upload_page.select_file(file_path)
    upload_page.upload_file()
    upload_page.assert_upload_success(filename)


def test_upload_without_file(upload_page):
    upload_page.open_page_url()
    upload_page.upload_file()
    upload_page.assert_upload_validation_msg(msg="No file selected")


@pytest.mark.skip(reason="Absent requirements")
def test_upload_invalid_files(upload_page):
    pass


def test_drag_and_drop_file(upload_page):
    file_path = TEST_DATA_PATH / "simple_image.jpeg"
    upload_page.open_page_url()
    upload_page.drag_and_drop_file(file_path)
    upload_page.assert_upload_success("simple_image.jpeg")


def test_change_upload_file(upload_page):
    file_path = TEST_DATA_PATH / "simple_image.jpeg"
    file_path_edited = TEST_DATA_PATH / "sample_min_size.txt"
    upload_page.open_page_url()
    upload_page.select_file(file_path)
    upload_page.select_file(file_path_edited)
    upload_page.upload_file()
    upload_page.assert_upload_success("sample_min_size.txt")
