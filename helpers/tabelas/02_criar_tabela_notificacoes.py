import dbf
import os


if not os.path.exists("./data/notificacoes.dbf"):
    dbf.Table(
        filename="./data/notificacoes.dbf",
        field_specs="CODGRUPO N(20,0);EMPR N(10,0); CODFUN N(10,0); DTNOTIFIC C(50); DSNOTIFIC C(150); ENVIADA N(1, 0)",  # noqa: E501
        dbf_type="vfp",
        codepage=0xF0,
    )
