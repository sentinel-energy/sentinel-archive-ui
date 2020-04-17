import re

import pandas as pd
from pandas.testing import assert_frame_equal

import docassemble.sarkui.io as _io


def compare_cols_transposed(txttbl, df):
    """after transpose, nrows = ncols; in txt form, ncols + sep + header"""
    return len(txttbl.splitlines()) == len(df.columns) + 2


def check_md_flavour(txttbl, df, flavour, index=False):
    sep = txttbl.splitlines()[1]
    ncols = len(df.columns) + int(index)  # index adds a column
    if flavour == "presto":
        pattern = re.compile(("-+\\+" * ncols)[:-2])
    elif flavour == "php":
        pattern = re.compile(("-+\\|" * ncols)[:-2])
    else:
        raise ValueError(f"unknown flavour: {flavour}")
    return pattern.match(sep)


def test_csv_sample(csvfile):
    df = _io.csv_sample(csvfile, nrows=3)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3  # nrows


def test_csv_preview(csvfile):
    txttbl = _io.csv_preview(csvfile, nrows=5)
    ref_df = _io.csv_sample(csvfile, nrows=5)
    assert compare_cols_transposed(txttbl, ref_df)


def test_csv_dtypes(csvfile):
    txttbl = _io.csv_dtypes(csvfile)
    ref_df = _io.csv_sample(csvfile)
    assert compare_cols_transposed(txttbl, ref_df)


def test_df_dtypes(csvfile):
    df = _io.df_dtypes(_io.csv_sample(csvfile))
    # pd.Series -> pd.DataFrame
    assert isinstance(df, pd.DataFrame)
    # column name, dtype
    assert len(df.columns) == 2
    assert tuple(df.columns) == ("columns", "types")


def test_df_markdown(csvfile):
    df = _io.csv_sample(csvfile)
    txttbl = _io.df_markdown(df)
    # check: presto format, no index
    assert check_md_flavour(txttbl, df, flavour="presto")


def test_dfT_markdown(csvfile):
    df = _io.csv_sample(csvfile)
    txttbl = _io.dfT_markdown(df)
    # check: transposed, php format, no index
    assert check_md_flavour(txttbl, df.T, flavour="php")


def test_presto_to_php_md():
    df = pd.DataFrame([[1, 2, 3], [0, 9, 8]], columns=tuple("abc"))
    txttbl = df.to_markdown(tablefmt=_io._MD_TABLEFMT)
    assert check_md_flavour(txttbl, df, flavour="presto", index=True)
    txttbl2 = _io._presto_to_php_md(txttbl)
    assert check_md_flavour(txttbl2, df, flavour="php", index=True)


def test_df_html():
    df = pd.DataFrame([[1, 2, 3], [0, 9, 8]], columns=tuple("abc"))
    htmltbl = _io.df_html(df)
    df_roundtrip = pd.read_html(htmltbl, index_col=0)[0]
    assert_frame_equal(df, df_roundtrip)
