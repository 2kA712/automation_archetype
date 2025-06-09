# SAMPLE API TEST CLASS
import pytest

from resources.apis.sample_groups import Groups
from tests.conftest import config
from utils.enums.api import ApiResponseStatus
from utils.schema_validator import validate_json_schema


class TestGroup:

    @pytest.mark.API
    @pytest.mark.SMOKE
    @pytest.mark.REGRESSION
    def test_api_get_group_happy_path(self, config):
        group = Groups(config)
        result = group.get_groups()

        assert result['status']['responseStatus'] == ApiResponseStatus.SUCCESS
        assert validate_json_schema(result, "groups/get_all_groups")

# ---------------------------------- Negative Tests ------------------------------------------------------

    @pytest.mark.API
    @pytest.mark.SMOKE
    @pytest.mark.REGRESSION
    def test_api_get_group_by_invalid_uuid(self, config):
        group_uuid = 'invalid uuid here'

        group = Groups(config)
        result = group.get_groups_by_uuid(group_uuid)

        assert result['status']['responseStatus'] == ApiResponseStatus.FAIL
        assert validate_json_schema(result, "groups/get_a_group")
