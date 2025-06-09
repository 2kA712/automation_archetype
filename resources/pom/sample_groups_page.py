from playwright.sync_api import Page, Locator, expect

from data.sample_groups_data import Group
from resources.pom.base_page import BasePage


class GroupsPage(BasePage):
    """
    Class representing a groups tab.

    This class inherits functionality from the BasePage class and provides
    specific methods for interacting with elements on a groups page.
    """
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.search_groups_input = page.locator("[data-qaid='Search Groups']")
        self.add_group_button = page.locator("[aria-label='Add Group']")
        self.add_group_main_button = page.locator("[btnstyle='mat-stroked-button']")
        self.group_name_input = page.locator("[data-qaid='tbpGroupName']")
        self.group_description_input = page.locator("textarea[data-qaid='tbpGroupDescription']")
        self.open_group_switcher = page.locator("[qaid='openGroup']")
        self.group_save_button = page.locator("[data-qaid='saveBtn']")
        self.import_csv_email_list_button = page.locator("[class='import-emails-btn']")
        self.single_user_email_input = page.locator("[data-qaid='tbpSingleUserEmail']")
        self.add_button = page.locator("//button/span[text()=' Add ']")
        self.search_emails_input = page.locator("[id='mat-input-22']")

    def group_by_name(self, group_name) -> Locator:
        """Dynamic locator for group in list by name"""
        return self.page.locator(f"//a[text()=' {group_name} ']")

    def _click_add_group_button(self) -> None:
        self.add_group_button.click()

    def _fill_group_info(self, group: Group) -> None:
        self._fill_group_name_input(group.name)
        self._fill_group_description_input(group.description)

    def _click_add_group_main_button(self) -> None:
        self.add_group_button.click()

    def _fill_search_groups_input(self, group_name: str) -> None:
        self.search_groups_input.clear()
        self.search_groups_input.fill(group_name)

    def _fill_group_description_input(self, group_description: str) -> None:
        self.group_description_input.fill(group_description)

    def _fill_group_name_input(self, group_name: str) -> None:
        self.group_name_input.click()
        self.group_name_input.clear()
        self.group_name_input.fill(group_name)

    def _switch_open_group_slider(self, state: bool) -> None:
        self.open_group_switcher.set_checked(state)

    def _click_import_csv_email_list_button(self) -> None:
        self.import_csv_email_list_button.click()

    def _fill_single_user_email_input(self, user_email: str) -> None:
        self.single_user_email_input.clear()
        self.single_user_email_input.fill(user_email)

    def _click_add_user_email_input(self) -> None:
        self.add_button.click()

    def _fill_search_emails_input(self, email: str) -> None:
        self.search_emails_input.clear()
        self.search_emails_input.fill(email)

    def _click_save_group_button(self) -> None:
        self.group_save_button.click()
        self.page.wait_for_load_state("load")

    def create_group(self, group_info: Group) -> None:
        """
        Creates a new group with the specified name and description.

        This method fills the group name and group description inputs with the provided values.

        :param group_info:
            (Group): The data for group creation
        :return:
            None
        """
        self._click_add_group_button()
        self._fill_group_info(group_info)
        self._click_save_group_button()

    def assert_group_in_list(self, group_name: str) -> None:
        """
        Asserts whether the specified group is present in the list.

        This method fills the search input with the provided group name
        to search for it in the list of groups.

        :param group_name:
            (str): The name of the group to search for.
        :return:
            None
        """
        self._fill_search_groups_input(group_name)
        expect(self.group_by_name(group_name)).to_be_visible()
