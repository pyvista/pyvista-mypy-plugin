import subprocess

import pytest
from pyvista_mypy_plugin import promote_type
import os
from pathlib import Path
import importlib.util

PLUGIN_PACKAGE = "pyvista_mypy_plugin"
TEST_DIR = str(Path(__file__).parent)
ROOT_DIR = str(Path(TEST_DIR).parent)
PLUGIN_DIR = str(Path(ROOT_DIR) / PLUGIN_PACKAGE)
MYPY_CONFIG_FILE = str(Path(TEST_DIR) / "mypy.ini")


@pytest.fixture
def decorated_single():
    @promote_type(float)
    class Foo: ...

    return Foo


@pytest.fixture
def decorated_double():
    @promote_type(float, str)
    class Foo: ...

    return Foo


def test_decorator(decorated_single, decorated_double):
    klass = decorated_single()
    assert isinstance(klass, decorated_single)

    klass = decorated_double()
    assert isinstance(klass, decorated_double)


def test_decorator_no_args():
    code = """
from pyvista_mypy_plugin import promote_type
@promote_type()
class Foo: ...
    """
    out = _run_mypy_code(code)
    stdout = str(out.stdout)
    match = "AssertionError: No arguments specified for decorator `promote_type`. At least one type argument expected."
    assert match in stdout


def _run_mypy_code(code):
    # Call mypy from the project root dir on the typing test case files
    # Calling from root ensures the config is loaded and imports are found
    # NOTE: running mypy can be slow, avoid making excessive calls
    cur = os.getcwd()
    if importlib.util.find_spec(PLUGIN_PACKAGE) is None:
        raise ModuleNotFoundError(
            f"Package {PLUGIN_PACKAGE.replace('_', '-')} is required for this test."
        )
    try:
        os.chdir(ROOT_DIR)

        return subprocess.run(
            [
                "mypy",
                "--config-file",
                MYPY_CONFIG_FILE,
                "--show-absolute-path",
                "--show-traceback",
                "-c",
                code,
            ],
            capture_output=True,
        )
    finally:
        os.chdir(cur)
