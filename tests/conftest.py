import os
import platform
from unittest import mock
import pytest
from selenium import webdriver

import eel.chrome as chm
import eel.edge as edge


@pytest.fixture
def driver():
    test_browser = os.environ.get("TEST_BROWSER", "auto").lower()

    if test_browser in ["auto", "chrome"]:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

        browser_path = chm.find_path()
        if browser_path and not browser_path.endswith(('Google Chrome', 'chrome.exe')):
            options.binary_location = browser_path

        try:
            driver = webdriver.Chrome(options=options)
        except Exception:
            # Fallback to Edge if Chrome is not available
            edge_options = webdriver.EdgeOptions()
            edge_options.add_argument('--headless=new')
            edge_options.add_argument('--disable-gpu')
            edge_options.add_argument('--no-sandbox')
            edge_path = edge.find_path()
            if edge_path:
                edge_options.binary_location = edge_path
            driver = webdriver.Edge(options=edge_options)

    elif test_browser == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        edge_path = edge.find_path()
        if edge_path:
            options.binary_location = edge_path
        driver = webdriver.Edge(options=options)
    else:
        raise ValueError(f"Unsupported browser for testing: {test_browser}")

    with mock.patch("eel.browsers.open"):
        yield driver

    try:
        driver.quit()
    except Exception:
        pass
