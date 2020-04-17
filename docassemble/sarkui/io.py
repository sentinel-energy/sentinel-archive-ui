from io import StringIO
from itertools import chain

import pandas as pd
from tabulate import tabulate

# markdown flavour for `tabulate` (closest to PHP)
_MD_TABLEFMT = "presto"
# format string for floats
_FLTFMT = ".3g"


def csv_sample(csvfile, nrows: int = 5):
    strstr = StringIO(csvfile.slurp())
    return pd.read_csv(strstr, nrows=nrows)


def csv_preview(csvfile, nrows: int = 5) -> str:
    return dfT_markdown(csv_sample(csvfile, nrows))


def csv_dtypes(csvfile) -> str:
    df = df_dtypes(csv_sample(csvfile))
    return fixtbl(df_markdown(df))


def df_dtypes(df):
    dtypes = df.dtypes.reset_index()
    dtypes.columns = ["columns", "types"]
    return dtypes


# dataframe converters
def df_markdown(df) -> str:
    return df.to_markdown(tablefmt=_MD_TABLEFMT, showindex=False)


def dfT_markdown(df) -> str:
    txttbl = tabulate(
        # transposed
        (chain([k], v) for k, v in df.to_dict(orient="list").items()),
        headers=tuple(chain(["columns"], map(str, range(len(df))))),
        # FIXME: doesn't respect float format due to heterogeneous columns
        floatfmt=_FLTFMT,
        tablefmt=_MD_TABLEFMT,
    )
    return fixtbl(txttbl)


def _presto_to_php_md(txt: str) -> str:
    """Convert Markdown flavours: Presto to PHP"""
    return txt.replace("-+-", "-|-")


fixtbl = _presto_to_php_md


def df_html(df) -> str:
    return df.to_html(float_format=lambda x: f"{{:{_FLTFMT}}}".format(x))
