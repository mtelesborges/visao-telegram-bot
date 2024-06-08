import dbf
import os


if not os.path.exists("./data/ponto.dbf"):
    dbf.Table(
        filename="./data/ponto.dbf",
        field_specs="EMPR N(10,0); CODFUN N(10,0); DTPONTO C(50); OBS C(150); FOTO C(50); LOCAL C(250)",  # noqa: E501
        dbf_type="vfp",
        codepage=0xF0,
    )
