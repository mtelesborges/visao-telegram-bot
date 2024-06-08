import dbf
import os
from configs.logger import logger


def registrar_ponto(
    codigo_empresa: int,
    codigo_funcionario: int,
    data: str,
    observacao: str,
    foto: str,
    localizacao: str,
    texto_foto: str,
):
    logger.info("Registrando ponto")
    if not os.path.exists("./data/ponto.dbf"):
        table = dbf.Table(
            filename="./data/ponto.dbf",
            field_specs="EMPR N(10,0); CODFUN N(10,0); DTPONTO C(50); OBS C(150); FOTO C(50); LOCAL C(50); DSFOTO C(150)",  # noqa: E501
            dbf_type="vfp",
            codepage=0xF0,
        )

    table = dbf.Table(filename="./data/ponto.dbf")

    with table:
        table.append(
            (
                codigo_empresa,
                codigo_funcionario,
                data,
                observacao,
                foto,
                localizacao[:250],
                texto_foto[:250],
            )
        )
