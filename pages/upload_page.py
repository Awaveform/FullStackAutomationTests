from pathlib import Path

from playwright.sync_api import Page, expect

from utilities.env_settings import env_settings


class UploadPage:
    """
    Page Object Model for the file upload page.

    Exposes methods to interact with:
    - direct file selection and upload
    - drag-and-drop upload
    - upload result validation
    """

    def __init__(self, page: Page) -> None:
        """
        Initializes locators and target URL for the upload page.

        :param page: Playwright Page instance
        """

        self.page = page
        self.url = env_settings.UI_BASE + "upload"
        self.file_input = page.locator("#file-upload")
        self.upload_button = page.locator("#file-submit")
        self.success_header = page.locator("h3")
        self.uploaded_files_message = page.locator("#uploaded-files")
        self.drop_area = page.locator("div.example")
        self.validation_message = page.locator("###")  # Placeholder selector

    def open_page_url(self) -> None:
        """
        Navigates to the upload page.
        """

        self.page.goto(self.url)

    def select_file(self, file_path: Path) -> None:
        """
        Selects a file using the file input element.

        :param file_path: Path to the file to be uploaded
        """

        self.file_input.set_input_files(file_path)

    def upload_file(self) -> None:
        """
        Clicks the upload button to submit the selected file.
        """

        self.upload_button.click()

    def drag_and_drop_file(self, file_path: Path) -> None:
        """
        Simulates a drag-and-drop file upload via fallback input.

        :param file_path: Path to the file to be uploaded
        """

        self.page.dispatch_event("body", "dragenter")
        self.page.dispatch_event("body", "dragover")
        self.file_input.set_input_files(file_path)
        self.upload_button.click()

    def assert_upload_success(self, file_name: str) -> None:
        """
        Asserts that upload success message and file name are shown.

        :param file_name: Expected uploaded file name
        """

        expect(self.success_header).to_have_text("File Uploaded!")
        expect(self.uploaded_files_message).to_have_text(file_name)

    def assert_upload_validation_msg(self, msg: str) -> None:
        """
        Asserts the presence of a specific validation message.

        :param msg: Expected validation error message text
        """

        expect(self.validation_message).to_have_text(msg)
