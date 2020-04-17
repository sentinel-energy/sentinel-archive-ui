from pathlib import Path
from unittest.mock import Mock

import pytest

_datadir = Path("tests/data")


@pytest.fixture
def csvfile():
    csvfile = Mock()
    csvfile.slurp.return_value = (_datadir / Path("sample-ok.csv")).read_text()
    return csvfile
