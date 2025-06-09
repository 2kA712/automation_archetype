import uuid
from datetime import datetime, timedelta
import random


class Generator:

    @classmethod
    def sequential_guid(cls, count: int):
        max_digits = len(str(count - 1))
        for i in range(1, count):
            last_digits = str(i).zfill(max_digits)
            zero_prefixed = '0' * (32 - max_digits)
            yield (f'{zero_prefixed[:8]}-{zero_prefixed[8:12]}-'
                   f'{zero_prefixed[12:16]}-{zero_prefixed[16:20]}-'
                   f'{zero_prefixed[20:32-len(last_digits)]}{last_digits}')

    @classmethod
    def unique_email(cls, base: str = 'Automation', domain: str = 'TestAutomation.com') -> str:
        unique_id = uuid.uuid4().hex[:8]
        return f'{base}_{unique_id}@{domain}'

    @classmethod
    def random_future_date(cls, days_range: int = 700, date_format: str = '%Y-%m-%d') -> str:
        today = datetime.today()
        future_date = today + timedelta(days=random.randint(0, days_range))
        return future_date.strftime(date_format)


def main():
    email = Generator.unique_email()
    print(email)


if __name__ == '__main__':
    main()
