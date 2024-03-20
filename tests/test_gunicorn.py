import sys
from unittest import mock

import pytest


@pytest.mark.skipif(sys.platform == "win32", reason="Windows doesn't have what it takes.")
def test_config_imports():
    from gunicorn.app.wsgiapp import run

    argv = ["gunicorn", "--check-config", "flaskapp", "-c", "src/gunicorn.conf.py"]

    with mock.patch.object(sys, "argv", argv):
        with pytest.raises(SystemExit) as excinfo:
            run()

    assert excinfo.value.args[0] == 0
