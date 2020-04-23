from typing import Dict, List

from docassemble.sarkui.io import df_markdown


_EDIT_FLAG_FMT = "{name}['{col}'].edit"


def df_schema(df, schema):
    # schema: DADict
    schema.new(df.columns)
    for col, dtype in df.dtypes.items():
        schema[col].dtype = str(dtype)
        schema[col].edit = False
    schema.gathered = True
    return schema


def df_schema_edit_flags(schema) -> List[Dict[str, str]]:
    return [
        {
            k: _EDIT_FLAG_FMT.format(name=schema.instanceName, col=k),
            "datatype": "yesno",
        }
        for k, v in schema.items()
    ]


def df_schema_prompt(df, schema):
    df = df.dtypes.reset_index().assign(
        edit=lambda _df: [
            _EDIT_FLAG_FMT.format(name=schema.instanceName, col=col)
            for col in _df.iloc[:, 0]
        ]
    )
    # NOTE: column headers can't be empty
    df.columns = ["Columns", "Types", "Edit (Y/N)"]
    return df_markdown(df)
