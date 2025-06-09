from playwright.sync_api import Page, Locator, expect
from utils.enums.ui import Tabs, SubPageMenu


class BasePage:
    """
    Base class for page objects
    """

    def __init__(self, page: Page):
        self.page = page
        self.confirm_button = page.locator("button[data-qaid='confirmText']")
        self.cancel_button = page.locator("button[data-qaid='cancelText']")
        self.footer_popup = page.locator("[class='mat-simple-snack-bar-content']")
        self.account_button = page.locator('[data-qaid="accountBtn"]')

    def navigate(self, url: str) -> None:
        """
        Navigate to the specified URL.
        :param url: The URL to navigate to.
        :return:
        """
        self.page.goto(url)

    def get_title(self) -> str:
        """
        Get the title of the current page.
        :return:
            str: The title of the current page.
        """
        return self.page.title()

    def navigate_to_tab(self, tab: Tabs) -> None:
        """
        Navigate to the specified tab.
        :param tab:
            Tabs: The tab to navigate to.
        :return:
        """
        if not self.is_tab_selected(tab):
            self.page.wait_for_selector("[class='mat-simple-snack-bar-content']", state="detached")
            self.page.click(tab.selector)
            self.page.wait_for_load_state("load", timeout=1_000)

    def navigate_to_sub_page(self, sub_page: SubPageMenu) -> None:
        """
        Navigate to the specified sub page.
        :param sub_page:
            str: The sub page to navigate to.
        :return:
        """
        self.page.wait_for_load_state("load", timeout=1_000)
        self.page.wait_for_selector('[data-qaid="accountBtn"]', state="detached")
        self.account_button.click()
        self.page.click(sub_page.selector)

    def is_tab_selected(self, tab: Tabs) -> bool:
        """
        Check if the specified tab is selected.

        :param tab:
            Tabs: The tab to check.
        :return:
             bool: True if the tab is selected, False otherwise.
        """
        return self.page.get_attribute(tab.selector, "aria-current") == "page"

    @staticmethod
    def get_shadow_input_text(selector: Locator) -> str:
        """
        Gets the text from the shadow input selector

        :param selector:
            Locator: The selector of input field
        :return:
            (str): The text of the input selector
        """
        return selector.input_value()

    @staticmethod
    def set_checked(checked: bool, mat_checkbox_selector: Locator) -> None:
        """
        Check the checkbox if the state is True, otherwise uncheck it.

        :param mat_checkbox_selector:
            (Locator): The selector of the checkbox
        :param checked:
            (bool): State of the checkbox locator
        :return:
            None
        """
        if mat_checkbox_selector.evaluate('el => el.classList.contains("mat-checkbox-checked")') != checked:
            mat_checkbox_selector.evaluate('el => el.firstChild.click()')
        else:
            pass

    def click_modal_confirm_button(self) -> None:
        """
        Clicks the modal confirm button.
        :return:
            None
        """
        self.confirm_button.click()

    def click_modal_cancel_button(self) -> None:
        """
        Clicks the modal cancel button.
        :return:
            None
        """
        self.cancel_button.click()

    @staticmethod
    def assert_element_is_displayed(selector: Locator, expected_status: bool = True) -> None:
        """
        Asserts whether an element identified by the given selector is displayed or not.

        :param selector:
            (Locator): The locator of the element to check.
        :param expected_status:
            (bool): The expected display status of the element
            (True for displayed, False for not displayed).

        :return:
        """
        if selector.is_visible() != expected_status:
            raise AssertionError()

    @staticmethod
    def assert_element_is_checked(selector: Locator, expected_status: bool = True) -> None:
        """
        Asserts whether an element identified by the given selector is checked or not.

        :param selector:
            (Locator): The locator of the element to check.
        :param expected_status:
            (bool): The expected display status of the element
            (True for checked, False for not checked).

        :return:
        """
        if selector.is_checked() != expected_status:
            raise AssertionError()

    @staticmethod
    def assert_text_in_element(element: Locator, text: str) -> None:
        """
        Asserts whether the given element contains the specified text.

        :param element:
            (Locator): The locator of the element to check.
        :param text:
            (str): The text to search for in the element.

        :return:
            None
        """
        expect(element).to_contain_text(text, use_inner_text=True)

    @staticmethod
    def assert_is_element_expanded(element: Locator, expected_status: bool = True) -> bool:
        """
        Asserts whether an element identified by the given selector is expanded or not.

        :param element:
            (Locator): The locator of the element to check.
        :param expected_status:
            (bool): The expected display status of the element
            (True for expanded, False for not expanded).

        :return:
            None
        """
        if element.evaluate('el => el.classList.contains("mat-expanded")') != expected_status:
            return not expected_status

    def assert_popup_is_displayed_with_text(self, text: str) -> None:
        """
        Asserts whether the popup is displayed with the specified text.

        :param text:
            (str): The text to search for in the popup.

        :return:
            None
        """
        self.assert_text_in_element(self.footer_popup, text)
