# swagger pages:
# https://time-based-parking-query-service.dev.link.t2systems.com/swagger-ui/index.html#/
# https://time-based-parking-service.dev.link.t2systems.com/swagger-ui/index.html
from resources.apis.base_api import BaseApi


class Groups(BaseApi):

    def __init__(self, config):
        """Constractor for group object.
        :param config: environment config values.
        """

        super().__init__(config)
        self.endpoint = 'groups'

    def get_groups(self, customer_id=None, group_name=None, pageable=None):
        """Getting list of groups.
        :param customer_id: customer id if not provided default config.customer_id will be used.
        :param group_name: name of specific group (optional).
        :param pageable: page size and sorting.
        :return: response json.
        """

        customer_id = customer_id if customer_id else self.customer_id
        pageable = pageable if pageable else self.pageable

        query_param = {
            'customerId': customer_id,
            'groupName': group_name,
            'pageable': pageable
        }

        return self.get(self.api_base_query_url, self.endpoint, query_param)

    def get_groups_by_uuid(self, group_uuid, customer_id=None):
        """Getting one group by uuid.
        :param group_uuid: group uuid.
        :param customer_id: customer id if not provided default config.customer_id will be used.
        :return: response json.
        """

        customer_id = customer_id if customer_id else self.customer_id

        query_param = {
            'customerId': customer_id
        }

        return self.get(self.api_base_query_url, f'{self.endpoint}/{group_uuid}', query_param)

    def get_group_emails(self, group_uuid, customer_id=None, email=None, pageable=None):
        """Getting group email address.
        :param group_uuid: group uuid.
        :param customer_id: customer id if not provided default config.customer_id will be used.
        :param email: email address(optional).
        :param pageable: page size and sorting.
        :return: response json.
        """

        customer_id = customer_id if customer_id else self.customer_id
        pageable = pageable if pageable else self.pageable

        query_param = {
            'customerId': customer_id,
            'emailaddress': email,
            'pageable': pageable
        }

        return self.get(self.api_base_query_url, f'{self.endpoint}/{group_uuid}/emails', query_param)

    def get_group_verification_fields(self, customer_id=None, pageable=None):
        """Getting verification fields based on customer id.
        :param customer_id: customer id if not provided default config.customer_id will be used.
        :param pageable: page size and sorting.
        :return: response json.
        """

        pageable = pageable if pageable else self.pageable
        customer_id = customer_id if customer_id else self.customer_id

        query_param = {
            'customerId': customer_id,
            'pageable': pageable
        }

        return self.get(self.api_base_query_url, f'{self.endpoint}/verificationfields', query_param)

    def get_group_classifications(self, customer_id=None, pageable=None):
        """Getting classifications based on customer id.
        :param customer_id: customer id if not provided default config.customer_id will be used.
        :param pageable: page size and sorting.
        :return: response json.
        """

        pageable = pageable if pageable else self.pageable
        customer_id = customer_id if customer_id else self.customer_id

        query_param = {
            'customerId': customer_id,
            'pageable': pageable
        }

        return self.get(self.api_base_query_url, f'{self.endpoint}/classifications', query_param)

    def update_group(self, group_uuid, pay_load):
        """Updating group.
        :param group_uuid: specific group uuid to be updated.
        :param pay_load: changes.
        :return: response json.
        """

        return self.put(url=self.api_base_url, endpoint=f'{self.endpoint}/{group_uuid}', data=pay_load)

    def create_group(self, pay_load):
        """Create group in tempo.
        :param pay_load: group json payload.
        :return: response json.
        """

        return self.post(url=self.api_base_url, endpoint=self.endpoint, data=pay_load)

    def add_emails_to_group(self, group_uuid, pay_load):
        """Adding email address to a specific group.
        :param group_uuid: specific group uuid to be added into.
        :param pay_load: changes.
        :return: response json.
        """

        return self.patch(url=self.api_base_url, endpoint=f'{self.endpoint}/{group_uuid}/emails', data=pay_load)
