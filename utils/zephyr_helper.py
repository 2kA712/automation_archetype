import jwt
import hashlib
import time
import requests
import os
from urllib.parse import urlencode, urlparse, parse_qsl


class ZephyrHelper:
    """
    A helper class for Zephyr .
    """
    def __init__(self, config):
        self.zephyr_config = config
        self.access_key = self.zephyr_config['access_key']
        self.secret_key = self.zephyr_config['secret_key']
        self.account_id = self.zephyr_config['account_id']
        self.project_id = self.zephyr_config['project_id']
        self.version_id = self.zephyr_config['version_id']
        self.jwt_expire = 3600
        self.base_url = self.zephyr_config['zephyr_base_url']
        self.base_api_path = self.zephyr_config['zephyr_api_path']

    def generate_jwt_token(self, canonical_path: str, method: str) -> str:
        """
        Generate a JSON Web Token (JWT) for authenticating API requests.

        Args:
            canonical_path (str): The canonical path of the API endpoint.
            method (str): The HTTP method of the API request.

        Returns:
            str: The generated JWT.
        """
        payload_token = {
            'sub': self.account_id,
            'qsh': self.calculate_qsh(canonical_path, method),
            'iss': self.access_key,
            'exp': int(time.time()) + self.jwt_expire,
            'iat': int(time.time())
        }
        return jwt.encode(payload_token, self.secret_key, algorithm='HS256').strip()

    @staticmethod
    def calculate_qsh(canonical_path: str, method: str) -> str:
        """
        Calculate the Query String Hash (QSH) for the given canonical path and method.

        Args:
            canonical_path (str): The canonical path of the API endpoint.
            method (str): The HTTP method of the API request.

        Returns:
            str: The calculated QSH.
        """
        parsed_url = urlparse(canonical_path)
        path = parsed_url.path
        query_string = urlencode(sorted(parse_qsl(parsed_url.query)))
        request = f'{method.upper()}&{path}&{query_string}'
        print(f"QSH raw string: {request}")  # Debugging line to print the raw string
        return hashlib.sha256(request.encode('utf-8')).hexdigest()

    def headers(self, canonical_path: str, method: str) -> dict:
        """
        Generate the headers for an API request.

        Args:
            canonical_path (str): The canonical path of the API endpoint.
            method (str): The HTTP method of the API request.

        Returns:
            dict: The generated headers.
        """
        content_type = 'text/plain' if method == 'GET' else 'application/json'
        return {
            'Authorization': 'JWT ' + self.generate_jwt_token(canonical_path, method),
            'Content-Type': content_type,
            'zapiAccessKey': self.access_key
        }

    def get_test_cycles(self, project_id: str) -> requests.Response:
        """
        Get the test cycles for the given project ID.

        Args:
            project_id (str): The ID of the project.

        Returns:
            requests.Response: The response from the API.
        """
        method = 'GET'
        endpoint = f'cycles/search?projectId={project_id}&versionId=21132'
        canonical_path = self.base_api_path + endpoint
        url = self.base_url + canonical_path
        response = requests.get(url, headers=self.headers(canonical_path, method))
        return response

    def create_test_cycle(self, cycle_name: str) -> dict:
        """
        Create a new test cycle with the given name.

        Args:
            cycle_name (str): The name of the test cycle.

        Returns:
            dict: The response from the API request.

        Raises:
            requests.exceptions.RequestException: If there was an error making the API request.
        """
        try:
            method = "POST"
            endpoint = 'cycle'
            canonical_path = self.base_api_path + endpoint
            url = self.base_url + canonical_path
            payload = {
                "clonedCycleId": None,
                "name": cycle_name,
                "build": "",
                "environment": "",
                "description": "",
                "startDate": "",
                "endDate": "",
                "projectId": self.project_id,
                "versionId": self.version_id
            }
            response = requests.post(url, headers=self.headers(canonical_path, method), json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise e

    def add_test_case_to_cycle(self, cycle_id: str, issue_ids: list) -> bytes:
        """
        Add the given test cases to the test cycle with the given ID.

        Args:
            cycle_id (str): The ID of the test cycle.
            issue_ids (list): The IDs of the test cases to add.

        Returns:
            bytes: The response content from the API request.

        Raises:
            requests.exceptions.RequestException: If there was an error making the API request.
        """
        try:
            method = "POST"
            endpoint = f'executions/add/cycle/{cycle_id}'
            canonical_path = self.base_api_path + endpoint
            url = self.base_url + canonical_path
            payload = {
                "issues": issue_ids,
                "method": 1,
                "projectId": self.project_id,
                "versionId": -1,
            }
            response = requests.post(url, headers=self.headers(canonical_path, method), json=payload)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            raise e

    def get_executions_by_cycle(self, cycle_id: str, issue_ids: list) -> dict:
        """
        Get the executions for the given test cases in the test cycle with the given ID.

        Args:
            cycle_id (str): The ID of the test cycle.
            issue_ids (list): The IDs of the test cases.

        Returns:
            dict: A dictionary of test case IDs and their corresponding execution IDs and issue IDs.

        Raises:
            requests.exceptions.RequestException: If there was an error making the API request.
        """
        try:
            method = "GET"
            endpoint = f'executions/search/cycle/{cycle_id}?projectId={self.project_id}&versionId={self.version_id}'
            canonical_path = self.base_api_path + endpoint
            url = self.base_url + canonical_path
            response = requests.get(url, headers=self.headers(canonical_path, method))
            response.raise_for_status()
            executions = response.json()['searchObjectList']
            execution_dict = {execution['issueKey']: (execution['execution']['id'], execution['execution']['issueId'])
                              for execution in executions if execution['issueKey'] in issue_ids}
            return execution_dict
        except requests.exceptions.RequestException as e:
            raise e

    def update_test_results(self, issue_execution_tuple: tuple, cycle_id: str, status_id: int, comment=None):
        """
        Update the test results for the given execution and status.

        Args:
            issue_execution_tuple (tuple): A tuple containing the issue ID and execution ID.
            cycle_id (str): The ID of the test cycle.
            status_id (str): The ID of the status.
            comment (str, optional): The comment to include in the request. Defaults to None.

        Returns:
            None

        Raises:
            requests.exceptions.RequestException: If there was an error making the API request.
        """
        try:
            method = "PUT"
            execution_id, issue_id = issue_execution_tuple
            endpoint = f'execution/{execution_id}'
            canonical_path = f'{self.base_api_path}{endpoint}'

            url = self.base_url + canonical_path

            payload = {
                "status": {"id": status_id},
                "id": execution_id,
                "projectId": self.project_id,
                "issueId": issue_id,
                "cycleId": cycle_id,
                "versionId": -1,
                "comment": "Failed due to: " + comment if comment else "Automation execution",
                "assigneeType": "currentUser",
                "assignee": "712020:e75707b5-5bb4-417a-80ee-a53f4333792d"
            }
            response = requests.put(url, headers=self.headers(canonical_path, method), json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f'RequestException: {e}')
            raise e

    def upload_attachment(self, file_path: str, issue_execution_tuple: tuple, cycle_id: str) -> dict:
        """
        Uploads an attachment for a given issue execution.

        Args:
            file_path (str): The path to the file to upload.
            issue_execution_tuple (tuple): A tuple containing the issue ID and execution ID.
            cycle_id (str): The ID of the test cycle.

        Returns:
            dict: The JSON response from the upload.

        Raises:
            requests.exceptions.RequestException: If there was an error making the API request.
        """
        try:
            execution_id, issue_id = issue_execution_tuple
            method = "POST"
            canonical_path = (f"{self.base_api_path}attachment"
                              f"?issueId={issue_id}"
                              f"&versionId={self.version_id}"
                              f"&entityName=execution"
                              f"&cycleId={cycle_id}"
                              f"&entityId={execution_id}"
                              f"&comment=Automation"
                              f"&projectId={self.project_id}")
            url = self.base_url + canonical_path

            # Generate headers without Content-Type as it will be set by requests when using files
            headers = self.headers(canonical_path, method)
            headers.pop('Content-Type', None)

            with open(file_path, 'rb') as file:
                files = {'file': (os.path.basename(file_path), file)}
                response = requests.post(url, headers=headers, files=files)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if e.response:
                raise f'Response content: {e.response.content}'
            raise f'Failed to upload attachment. RequestException: {e}'
