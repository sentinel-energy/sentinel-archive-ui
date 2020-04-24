import re

from glom import glom, T
import pytest

from docassemble.sarkui.io import csv_sample
from docassemble.sarkui.schema import (
    df_schema_flags,
    df_schema_flags_prompt,
    df_schema_dtype,
    df_fix_schema,
    _FLAG_FMT,
    _FIELD_FMT,
    _TYPES,
)


def test_df_schema_flags(csvfile, flags):
    df = csv_sample(csvfile)
    res = df_schema_flags(df, flags)
    assert glom(res, ["datatype"]) == ["yesno"] * len(res)
    # NOTE: index 0 relies on deterinistic dictionary order
    assert glom(res, [(tuple, "0")]) == df.columns.to_list()
    assert glom(res, [(T.values(), tuple, "0")]) == [
        _FLAG_FMT.format(name=flags.instanceName, col=col)
        for col in df.columns
    ]


def test_df_schema_flags_prompt(csvfile, flags):
    df = csv_sample(csvfile)

    hdr, hline, *txttbl = df_schema_flags_prompt(df, flags).splitlines()
    assert re.compile(("-+\\|" * 3)[:-2]).match(hline)

    col_sep = " +\\| +"
    cols_hdr = ["Columns", "Types", "Edit \\(Y/N\\)"]
    assert re.compile(col_sep.join(cols_hdr)).match(hdr.strip())

    ESCAPED_FMT = _FIELD_FMT.format(_FLAG_FMT).replace("[", "\\[")
    fields = [
        ESCAPED_FMT.format(name=flags.instanceName, col=col)
        for col in df.columns
    ]
    tbl_cells = zip(df.columns, map(str, df.dtypes), fields)
    assert all(
        re.compile(col_sep.join(cells)).match(row.strip())
        for cells, row in zip(tbl_cells, txttbl)
    )


def set_flags(flags, cols):
    # flag columns
    flagged_cols = [col for i, col in enumerate(cols) if i in [0, 3]]
    flags.update((col, True if col in flagged_cols else False) for col in cols)
    return flags, flagged_cols


def test_df_schema_dtype(csvfile, flags):
    df = csv_sample(csvfile)
    flags, flagged_cols = set_flags(flags, df.columns)
    res = df_schema_dtype(df, flags)
    assert glom(res, ["choices"]) == [_TYPES] * len(res)
    # NOTE: index 0 relies on deterinistic dictionary order
    assert glom(res, [(tuple, "0")]) == flagged_cols
    assert glom(res, [(T.values(), tuple, "0")]) == [
        _FLAG_FMT.format(name=flags.instanceName, col=col)
        for col in flagged_cols
    ]


def test_df_fix_schema(csvfile, flags):
    df = csv_sample(csvfile)
    flags, flagged = set_flags(flags, df.columns)
    # set flags to dtypes
    flags.update((col, "string") for col in flagged)
    df_t = df_fix_schema(df, flags).dtypes
    assert df_t[flagged].astype(str).to_list() == ["string"] * len(flagged)
