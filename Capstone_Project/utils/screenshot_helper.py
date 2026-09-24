"""
screenshot_helper.py
Utility for capturing and saving Selenium screenshots with timestamps.
"""

import os
import logging
from datetime import datetime

from config.config import SCREENSHOTS_DIR

logger = logging.getLogger(__name__)


def capture_screenshot(driver, step_name: str) -> str:
    """
    Capture a browser screenshot and save it to the screenshots directory.

    :param driver:     Active Selenium WebDriver instance.
    :param step_name:  Descriptive name for the step (used in filename).
    :return:           Absolute path of the saved screenshot file.
    """
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Sanitize step name for filesystem safety
    safe_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in step_name)
    filename  = f"{timestamp}_{safe_name}.png"
    filepath  = os.path.join(SCREENSHOTS_DIR, filename)

    try:
        driver.save_screenshot(filepath)
        logger.info(f"[Screenshot] Saved → {filepath}")
    except Exception as exc:
        logger.error(f"[Screenshot] Failed to save '{filepath}': {exc}")
        raise

    return filepath


def capture_full_page_screenshot(driver, step_name: str) -> str:
    """
    Attempt a full-page screenshot using JavaScript scroll-and-stitch.
    Falls back to a standard viewport screenshot if it fails.

    :param driver:     Active Selenium WebDriver instance.
    :param step_name:  Descriptive name for the step.
    :return:           Absolute path of the saved screenshot file.
    """
    try:
        # Scroll to top, set large window height, capture, then restore
        original_size = driver.get_window_size()
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, scroll_height + 100)
        path = capture_screenshot(driver, f"fullpage_{step_name}")
        driver.set_window_size(original_size["width"], original_size["height"])
        return path
    except Exception as exc:
        logger.warning(f"Full-page screenshot failed ({exc}), falling back to viewport.")
        return capture_screenshot(driver, step_name)
