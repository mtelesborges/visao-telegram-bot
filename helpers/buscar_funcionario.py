import dbf
from typing import Dict
from configs.logger import logger


def buscar_funcionario(codigo_empresa: int, codigo_funcionario: int) -> Dict:
    logger.info("Buscando funcionário...")
    table = dbf.Table("./data/cadponto.dbf")
    with table:
        procod_idx = table.create_index(lambda rec: (rec.EMPR, rec.CODFUN))
        match = procod_idx.search(match=(codigo_empresa, codigo_funcionario))
        if len(match) == 0:
            logger.info("Nenhum funcionário localizado...")
            return None
        logger.info("Funcionário localizado...")
        return match[0]
