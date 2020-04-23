from pathlib import Path
from random import choices
from string import ascii_letters
from unittest.mock import Mock, MagicMock

import pytest

_datadir = Path("tests/data")


@pytest.fixture
def csvfile():
    # mock a DAFile instance
    csvfile = Mock()
    csvfile.slurp.return_value = (_datadir / Path("sample-ok.csv")).read_text()
    return csvfile


@pytest.fixture
def schema():
    # mock a DADict instance
    dadict_attrs = dir(dict) + ["new", "instanceName", "gathered"]
    schema = MagicMock(spec_set=dadict_attrs)
    schema.instanceName = "".join(choices(ascii_letters, k=5))  # DAObject name

    data = {}
    schema.new.side_effect = lambda ks: data.update((k, MagicMock) for k in ks)
    schema.__getitem__.side_effect = data.__getitem__
    schema.__setitem__.side_effect = data.__setitem__
    schema.keys.side_effect = data.keys
    schema.items.side_effect = data.items

    def _str():
        ks = list(map(str, data.keys()))
        return f"{' '.join(ks[:-1])} and {ks[-1]}"

    schema.__str__.side_effect = _str
    return schema
