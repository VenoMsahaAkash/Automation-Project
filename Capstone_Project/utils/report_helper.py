"""
report_helper.py
Utility functions for generating and enhancing the execution report.
"""

import json
import logging
import os
from datetime import datetime

from config.config import REPORTS_DIR, SCREENSHOTS_DIR

logger = logging.getLogger(__name__)


def get_report_path(filename: str = "execution_report.html") -> str:
    """Return the full path to the HTML report file."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    return os.path.join(REPORTS_DIR, filename)


def log_test_result(test_name: str, status: str, details: str = "",
                    screenshot_path: str = "") -> dict:
    """
    Build a structured result dictionary for a single test.

    :param test_name:       Name of the test scenario.
    :param status:          'PASS', 'FAIL', or 'SKIP'.
    :param details:         Extra information about the result.
    :param screenshot_path: Path to associated screenshot (optional).
    :return:                Result dictionary.
    """
    result = {
        "test_name":       test_name,
        "status":          status,
        "timestamp":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "details":         details,
        "screenshot_path": screenshot_path,
    }
    logger.info(f"[Report] {test_name} → {status}: {details}")
    return result


def save_json_report(results: list[dict], filename: str = "test_results.json"):
    """
    Save a list of test result dictionaries to a JSON file in the reports directory.

    :param results:  List of result dicts from log_test_result().
    :param filename: Output filename (default: test_results.json).
    :return:         Path to the saved JSON file.
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)
    filepath = os.path.join(REPORTS_DIR, filename)

    report = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total":  len(results),
        "passed": sum(1 for r in results if r["status"] == "PASS"),
        "failed": sum(1 for r in results if r["status"] == "FAIL"),
        "skipped": sum(1 for r in results if r["status"] == "SKIP"),
        "results": results,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    logger.info(f"[Report] JSON report saved: {filepath}")
    return filepath


def list_screenshots() -> list[str]:
    """Return a list of all screenshot file paths in the screenshots directory."""
    if not os.path.exists(SCREENSHOTS_DIR):
        return []
    files = sorted(
        [
            os.path.join(SCREENSHOTS_DIR, f)
            for f in os.listdir(SCREENSHOTS_DIR)
            if f.lower().endswith(".png")
        ]
    )
    logger.info(f"[Report] Found {len(files)} screenshot(s).")
    return files


def print_summary(results: list[dict]):
    """Print a formatted test summary table to the console."""
    separator = "=" * 65
    print(f"\n{separator}")
    print("  CAPSTONE PROJECT — TEST EXECUTION SUMMARY")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(separator)
    print(f"  {'#':<4} {'Test Name':<38} {'Status':<8}")
    print("-" * 65)
    for i, r in enumerate(results, start=1):
        icon   = "✓" if r["status"] == "PASS" else ("✗" if r["status"] == "FAIL" else "~")
        status = r["status"]
        print(f"  {i:<4} {r['test_name']:<38} [{icon}] {status}")
    print(separator)
    passed  = sum(1 for r in results if r["status"] == "PASS")
    failed  = sum(1 for r in results if r["status"] == "FAIL")
    skipped = sum(1 for r in results if r["status"] == "SKIP")
    print(f"  Total: {len(results)}  |  Passed: {passed}  |  "
          f"Failed: {failed}  |  Skipped: {skipped}")
    print(f"{separator}\n")
