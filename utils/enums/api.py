from enum import Enum, StrEnum


class ApiResponseStatus(StrEnum):
    SUCCESS = 'Success'
    FAIL = 'Fail'

    def __str__(self):
        return str(self.value)
