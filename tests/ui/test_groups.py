# SAMPLE UI TEST
import pytest

from resources.pom.sample_login_page import LoginPage
from resources.pom.sample_groups_page import GroupsPage
from utils.enums.ui import Tabs
from data.sample_groups_data import Group


class TestGroupPage:

    @pytest.mark.UI
    @pytest.mark.SMOKE
    @pytest.mark.TEST_ID(id='TBPRK-1323')
    def test_add_group(page, config):
        """ Pages initialization """
        login_page = LoginPage(page)
        groups_page = GroupsPage(page)

        """ Data for test """
        group_data = Group.generate_base_group(config["tempo_configuration"].get("customer_id"))

        """ Test start """
        login_page.login()
        groups_page.navigate_to_tab(Tabs.GROUPS)
        groups_page.create_group(group_data)
        groups_page.assert_group_in_list(group_data.name)

        """ Test cleanup """
