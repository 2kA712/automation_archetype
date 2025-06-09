from enum import Enum, IntEnum


class Tabs(Enum):
    """
        Enumeration of dashboard items containing tab names and selectors.

        Each member represents a specific tab with an associated tab name and selector.

        Attributes:
            DASHBOARD: Represents the dashboard tab.
            GROUPS: Represents the groups tab.
    """
    DASHBOARD = ("Dashboard", '[id="mat-tab-link-0"]')
    GROUPS = ("Groups", '[id="mat-tab-link-1"]')

    def __init__(self, tab_name: str, selector: str):
        self.tab_name = tab_name
        self.selector = selector


class ContextMenuOptions(IntEnum):
    """
        Enumeration of menu options for a context menu dropdown.

        Each member represents a specific option with an associated index.

        Attributes:
            VIEW_IN_FULL_SCREEN: Option to view in full screen.
            PRINT_CHART: Option to print the chart.
            DOWNLOAD_PNG_IMAGE: Option to download as a PNG image.
            DOWNLOAD_JPEG_IMAGE: Option to download as a JPEG image.
            DOWNLOAD_PDF_DOCUMENT: Option to download as a PDF document.
            DOWNLOAD_SVG_VECTOR_IMAGE: Option to download as an SVG vector image.
            DOWNLOAD_CSV: Option to download as a CSV file.
            DOWNLOAD_XLS: Option to download as an XLS file.
            VIEW_DATA_TABLE: Option to view as a data table.
    """
    VIEW_IN_FULL_SCREEN = 0
    PRINT_CHART = 1
    DOWNLOAD_PNG_IMAGE = 2
    DOWNLOAD_JPEG_IMAGE = 3
    DOWNLOAD_PDF_DOCUMENT = 4
    DOWNLOAD_SVG_VECTOR_IMAGE = 5
    DOWNLOAD_CSV = 6
    DOWNLOAD_XLS = 7
    VIEW_DATA_TABLE = 8

    # TODO refactor to name, locator
    def __init__(self, position: int):
        self.position = position


class PricingScheduleType(Enum):
    """
        Enumeration of pricing schedule types.

        Each member represents a specific pricing schedule type along with its associated selector.

        Attributes:
            ALL: Represents all pricing schedule types.
            NORMAL: Represents normal pricing schedule type.
            SPECIAL: Represents special pricing schedule type.
    """
    ALL = ("All", '')
    NORMAL = ("Normal", '')
    SPECIAL = ("Special", '')

    def __init__(self, schedule_type: str, selector: str):
        self.schedule_type = schedule_type
        self.selector = selector


class TimeInterval(Enum):
    """
        Enumeration of time intervals.

        Each member represents a specific time interval along with its associated selector.

        Attributes:
            FIFTEEN_MINUTES: Represents a time interval of 15 minutes.
            THIRTY_MINUTES: Represents a time interval of 30 minutes.
            ONE_HOUR: Represents a time interval of 1 hour.
            TWO_HOURS: Represents a time interval of 2 hours.
            THREE_HOURS: Represents a time interval of 3 hours.
            FOUR_HOURS: Represents a time interval of 4 hours.
            SIX_HOURS: Represents a time interval of 6 hours.
            EIGHT_HOURS: Represents a time interval of 8 hours.
            TWELVE_HOURS: Represents a time interval of 12 hours.
            ONE_DAY: Represents a time interval of 1 day.

        Attributes:
            time_interval (str): The string representation of the time interval.
            selector (str): The selector associated with the time interval.
    """
    FIFTEEN_MINUTES = ("15 min", '')
    THIRTY_MINUTES = ("30 min", '')
    ONE_HOUR = ("1 hour", '')
    TWO_HOURS = ("2 hours", '')
    THREE_HOURS = ("3 hours", '')
    FOUR_HOURS = ("4 hours", '')
    SIX_HOURS = ("6 hours", '')
    EIGHT_HOURS = ("8 hours", '')
    TWELVE_HOURS = ("12 hours", '')
    ONE_DAY = ("1 day", '')

    def __init__(self, time_interval: str, selector: str):
        self.time_interval = time_interval
        self.selector = selector


class SubPageMenu(Enum):
    """
        Enumeration of sub-page menu options.

        Each member represents a specific sub-page menu option along with its associated selector.

        Attributes:
            MY_PROFILE: Represents the my profile sub-page menu option button.
            PAYMENT_HISTORY: Represents the payment history sub-page menu option button.
            MY_VEHICLE: Represents the my vehicle sub-page menu option button.
            ABOUT: Represents the about sub-page menu option button.
            CONTACT: Represents the contact sub-page menu option button.
            LOGOUT: Represents the logout menu option button.
    """
    MY_PROFILE = ("My Profile", '[data-qaid="My Profile"]')
    PAYMENT_HISTORY = ("Payment History", '[data-qaid="Payment History"]')
    MY_VEHICLE = ("My Vehicle", '[data-qaid="My Vehicles"]')
    FAQ = ("FAQ", '[data-qaid="FAQs"]')
    ABOUT = ("About", '[data-qaid="About"]')
    CONTACT = ("Contact", '[data-qaid="Contact"]')
    LOGOUT = ("Logout", '[data-qaid="Logout"]')

    def __init__(self, name: str, selector: str):
        self.name_ = name
        self.selector = selector
