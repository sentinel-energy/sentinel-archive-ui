from typing import Dict, List

from docassemble.sarkui.io import df_dtypes, df_markdown


_FLAG_FMT = "{name}['{col}']"
_FIELD_FMT = "[FIELD {}]"
# FIXME: should be imported from `sark`
_TYPES = ["datetime64", "Int64", "float", "bool", "string", "category"]


def df_schema_flags(df, flags) -> List[Dict[str, str]]:
    return [
        {
            col: _FLAG_FMT.format(name=flags.instanceName, col=col),
            "datatype": "yesno",
        }
        for col in df.columns
    ]


def df_schema_flags_prompt(df, flags):
    FIELD_FMT = _FIELD_FMT.format(_FLAG_FMT)
    df = df_dtypes(df).assign(
        edit=lambda _df: [
            FIELD_FMT.format(name=flags.instanceName, col=col)
            for col in _df.iloc[:, 0]
        ]
    )
    # NOTE: column headers can't be empty
    df.columns = ["Columns", "Types", "Edit (Y/N)"]
    return df_markdown(df)


def df_schema_dtype(df, flags) -> List[Dict[str, str]]:
    # TODO: conditional additional inputs, e.g. format string for timestamps
    # {
    #     "datetime_fmt_str": "datetime_fmt",
    #     "show if": {"variable": "dtype", "is": "datetime64"},
    # }
    return [
        {
            col: _FLAG_FMT.format(name=flags.instanceName, col=col),
            "choices": _TYPES,
        }
        for col in df.columns
        if flags[col]
    ]


def df_fix_schema(df, flags):
    return df.assign(
        **{col: df[col].astype(flag) for col, flag in flags.items() if flag}
    )
