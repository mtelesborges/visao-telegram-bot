import dbf
import os
from configs.logger import logger


def registrar_grupo(
    nome: str,
    codigo: str,
):
    logger.info("Registrando grupo")
    table = None
    if not os.path.exists("./data/grupos.dbf"):
        dbf.Table(
            filename="./data/grupos.dbf",
            field_specs="NOME C(150); CODIGO C(150); ATIVO C(1)",  # noqa: E501
            dbf_type="vfp",
        )
    else:
        table = dbf.Table(filename="./data/grupos.dbf")

    table = dbf.Table("./data/grupos.dbf")

    match = []

    with table:
        procod_idx = table.create_index(lambda rec: rec.CODIGO)
        match = procod_idx.search(match=codigo)

        if len(match) > 0:
            logger.info(f"Grupo já cadastrado: {nome}")
            return

        table.append((nome, codigo, "S"))
        logger.info(f"Grupo cadastrado: {nome}")
