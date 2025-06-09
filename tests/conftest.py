import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright
from utils.config_loader import ConfigLoader
from datetime import datetime
from utils.zephyr_helper import ZephyrHelper
import traceback


def pytest_addoption(parser):
    parser.addoption("--env",
                     action="store",
                     default="qa",
                     help="Environment to run tests against (qa, dev, prod)")
    parser.addoption("--browser-name",
                     action="store",
                     default=None,
                     help="Browser to run tests (chromium, firefox, webkit)")
    parser.addoption("--test-id",
                     action="store",
                     help="Run with specific id")
    parser.addoption("--push-to-zephyr",
                     action="store_true",
                     default=False,
                     help="Push test results to Zephyr")
    parser.addoption("--cycle-name",
                     action="store",
                     default=None,
                     help="Name of the test cycle to create or use")


@pytest.fixture(scope='session', autouse=True)
def load_config(pytestconfig):
    env = pytestconfig.getoption("--env")
    config_path = Path(__file__).parent / f'../configs/{env}.yaml'
    ConfigLoader.load_config(config_path)


@pytest.fixture(scope="session")
def config(pytestconfig):
    config = ConfigLoader.get_config()
    browser_name = pytestconfig.getoption("--browser-name")
    if browser_name:
        config['browser'] = browser_name
    print(f"Loaded config: {config}")
    return config


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(config, playwright):
    browser_type = config.get('browser', 'chromium')
    browser = playwright[browser_type].launch(headless=config.get('headless', True))
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


def pytest_collection_modifyitems(config, items):
    test_id = config.getoption("--test-id")
    if test_id:
        selected_items = []
        deselected_items = []
        for item in items:
            if test_id in [mark.kwargs.get('id') for mark in item.iter_markers(name='TEST_ID')]:
                selected_items.append(item)
            else:
                deselected_items.append(item)
        items[:] = selected_items
        config.hook.pytest_deselected(items=deselected_items)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        page = item.funcargs.get('page')
        if page:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_dir = Path(__file__).parent / '../screenshots'
            screenshot_dir.mkdir(exist_ok=True)
            screenshot_path = screenshot_dir / f"{item.nodeid.replace('::', '_')}_{timestamp}.png"
            page.screenshot(path=str(screenshot_path))
            # Store the screenshot path in the item
            item.screenshot_path = screenshot_path
            # Store the failure report in the item
            item.failure_report = report


def extract_relevant_stack_trace(longrepr):
    if isinstance(longrepr, tuple):
        # Handle case when longrepr is a tuple (e.g., (file, lineno, msg))
        return ''.join(traceback.format_exception(None, longrepr[2], None))
    elif hasattr(longrepr, 'reprtraceback'):
        # Handle case when longrepr is a detailed object
        return ''.join(longrepr.reprtraceback.__str__().splitlines(keepends=True)[-10:])  # get last 10 lines
    elif hasattr(longrepr, 'getrepr'):
        # Handle case when longrepr is a string or object with a getrepr
        return ''.join(longrepr.getrepr(style='short').splitlines(keepends=True)[-10:])  # get last 10 lines
    else:
        # Handle case when longrepr is a string or object with a repr
        return str(longrepr)


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    if not session.config.getoption("--push-to-zephyr"):
        return
    cycle_name = session.config.getoption("--cycle-name")
    if not cycle_name:
        cycle_name = f"Automation Run {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    config = ConfigLoader.get_config()['zephyr']
    zephyr_helper = ZephyrHelper(config)
    new_cycle = zephyr_helper.create_test_cycle(cycle_name)

    if not new_cycle:
        print("Failed to create or retrieve test cycle.")
        return

    cycle_id = new_cycle['id']
    issue_ids = []

    for item in session.items:
        test_case_key = None
        marker = item.get_closest_marker("TEST_ID")
        if marker and marker.kwargs.get('id'):
            test_case_key = marker.kwargs.get('id')
        if test_case_key:
            issue_ids.append(test_case_key)

    if issue_ids:
        add_cases_response = zephyr_helper.add_test_case_to_cycle(cycle_id, issue_ids)
        if not add_cases_response:
            print("Failed to add test cases to the cycle.")
            return

        execution_ids = zephyr_helper.get_executions_by_cycle(cycle_id, issue_ids)
        if execution_ids:
            for item in session.items:
                test_case_key = None
                marker = item.get_closest_marker("TEST_ID")
                if marker and marker.kwargs.get('id'):
                    test_case_key = marker.kwargs.get('id')
                if not test_case_key:
                    continue

                execution_id = execution_ids.get(test_case_key)
                if not execution_id:
                    continue
                comment = None
                status = 1 if item.rep_call.passed else 2  # 1 for pass, 2 for fail
                if hasattr(item, 'failure_report'):
                    screenshot_path = getattr(item, 'screenshot_path', None)
                    if screenshot_path:
                        with open(screenshot_path, 'rb') as f:
                            screenshot_data = f.read()
                if hasattr(item, 'rep_call') and item.rep_call.failed:
                    # Capture short stack trace from longrepr
                    comment = extract_relevant_stack_trace(item.rep_call.longrepr)
                zephyr_helper.update_test_results(execution_id, cycle_id, status, comment)

                screenshot_path = getattr(item, 'screenshot_path', None)

                if screenshot_path:
                    zephyr_helper.upload_attachment(str(screenshot_path), execution_id, cycle_id)
