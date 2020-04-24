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
def flags():
    # mock a DADict instance
    dadict_attrs = dir(dict) + ["new", "instanceName", "gathered"]
    dadict = MagicMock(spec_set=dadict_attrs)
    dadict.instanceName = "".join(choices(ascii_letters, k=5))  # DAObject name

    data = {}
    dadict.new.side_effect = lambda ks: data.update((k, MagicMock) for k in ks)
    dadict.__getitem__.side_effect = data.__getitem__
    dadict.__setitem__.side_effect = data.__setitem__
    dadict.keys.side_effect = data.keys
    dadict.items.side_effect = data.items
    dadict.update.side_effect = data.update

    def _str():
        ks = list(map(str, data.keys()))
        return f"{' '.join(ks[:-1])} and {ks[-1]}"

    dadict.__str__.side_effect = _str
    return dadict
