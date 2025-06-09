from playwright.sync_api import Page
from resources.pom.base_page import BasePage
from utils.config_loader import ConfigLoader


class LoginPage(BasePage):
    """
        Class representing a login page.

        This class initializes a login page object, which provides functionality
        for interacting with elements on a login page.

        Args:
            page (Page): The Page object from Playwright's sync API.
    """
    def __init__(self, page: Page):
        super().__init__(page)
        self.config = ConfigLoader.get_config()
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#kc-login")
        self.logout_pwa_button = page.locator('[data-qaid="Logout"]')

        self.logout_configuration_button = page.locator('[data-qaid="Log out"]')

    def login(self, username: str = None, password: str = None) -> None:
        """
        :param username: by default get from config
        :param password: by default get from config
        :return:
        """
        username = username or self.config['tempo_configuration'].get('username')
        password = password or self.config['tempo_configuration'].get('password')
        self.navigate(self.config['tempo_configuration'].get('base_ui_url'))
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def login_as_parking_user(self, username: str = None, password: str = None) -> None:
        """
        Logs in as a parking user with the given username and password.
        This function navigates to the base UI URL, fills in the username and password inputs with the provided or
        default values, and clicks the login button.
        Args:
            username (str, optional): The username to log in with. If not provided, the username from the configuration
            file will be used.
            password (str, optional): The password to log in with. If not provided, the password from the configuration
            file will be used.
        Returns:
            None
        """
        username = username or self.config['tempo_user'].get('username')
        password = password or self.config['tempo_user'].get('password')
        self.navigate(self.config['tempo_user'].get('base_ui_url'))
        self.page.wait_for_load_state("load", timeout=1_000)
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def logout_as_parking_user(self):
        self.page.click('[data-qaid="accountBtn"]')
        self.logout_pwa_button.click()

    def logout_as_configuration_user(self):
        self.page.click('[data-qaid="fullUserMenuBtn"]')
        self.logout_configuration_button.click()
