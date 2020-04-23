import re

from glom import glom, T

from docassemble.sarkui.io import csv_sample
from docassemble.sarkui.schema import (
    df_schema,
    df_schema_edit_flags,
    df_schema_prompt,
    _EDIT_FLAG_FMT,
)


def test_df_schema(csvfile, schema):
    df = csv_sample(csvfile)
    res = df_schema(df, schema)
    assert list(res.keys()) == list(df.columns)
    assert all(
        hasattr(v, "dtype") and hasattr(v, "edit") and v.edit is False
        for _, v in res.items()
    )
    assert res.gathered


def test_df_schema_edit_flags(csvfile, schema):
    df = csv_sample(csvfile)
    schema = df_schema(df, schema)
    res = df_schema_edit_flags(schema)
    assert list(glom(res, ["datatype"])) == ["yesno"] * len(res)
    assert glom(res, [(tuple, "0")]) == list(df.columns)
    assert glom(res, [(T.values(), tuple, "0")]) == [
        _EDIT_FLAG_FMT.format(name=schema.instanceName, col=col)
        for col in df.columns
    ]


def test_df_schema_prompt(csvfile, schema):
    df = csv_sample(csvfile)
    schema = df_schema(df, schema)

    header, headline, *txttbl = df_schema_prompt(df, schema).splitlines()
    assert re.compile(("-+\\|" * 3)[:-2]).match(headline)

    col_sep = " +\\| +"
    cols_hdr = ["Columns", "Types", "Edit \\(Y/N\\)"]
    assert re.compile(col_sep.join(cols_hdr)).match(header.strip())

    ESCAPED_FMT = _EDIT_FLAG_FMT.replace("[", "\\[")
    fields = [
        ESCAPED_FMT.format(name=schema.instanceName, col=col)
        for col in df.columns
    ]
    tbl_cells = zip(df.columns, map(str, df.dtypes), fields)
    assert all(
        re.compile(col_sep.join(cells)).match(row.strip())
        for cells, row in zip(tbl_cells, txttbl)
    )
