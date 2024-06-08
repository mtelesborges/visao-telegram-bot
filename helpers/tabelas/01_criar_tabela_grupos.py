import dbf
import os


if not os.path.exists("./data/grupos.dbf"):
    dbf.Table(
        filename="./data/grupos.dbf",
        field_specs="NOME C(150); CODIGO N(20, 0); ATIVO C(1)",  # noqa: E501
        dbf_type="vfp",
        codepage=0xF0,
    )
