"""Pytest configuration and fixtures."""

import pytest


def pytest_addoption(parser):
    """Add custom command line option to run email tests."""
    parser.addoption(
        "--run-email",
        action="store_true",
        default=False,
        help="Run email integration tests (requires SENDGRID_API_KEY)",
    )


def pytest_configure(config):
    """Register custom marker for email tests."""
    config.addinivalue_line(
        "markers", "email: Integration test that sends real email (use --run-email)"
    )


def pytest_collection_modifyitems(config, items):
    """Skip email tests unless --run-email flag is provided."""
    if config.getoption("--run-email"):
        # --run-email given in cli: do not skip email tests
        return
    skip_email = pytest.mark.skip(reason="need --run-email option to run")
    for item in items:
        if "email" in item.keywords:
            item.add_marker(skip_email)
