"""Basic import tests for the Pypacity package."""

import importlib

MODULES = [
    "pypacity",
    "pypacity.cable.cable",
    "pypacity.case.case",
    "pypacity.cigre601.cigre601",
    "pypacity.ieee738.ieee738",
    "pypacity.utils.solar",
]


def test_modules_can_be_imported() -> None:
    """Verify that the main package modules can be imported."""
    for module_name in MODULES:
        module = importlib.import_module(module_name)
        assert module is not None