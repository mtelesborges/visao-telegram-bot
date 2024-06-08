from datetime import datetime
from typing import Any

import dbf

from configs.logger import logger


def buscar_turno_funcionario(
        codigo_empresa: int, codigo_funcionario: int
) -> list[Any]:
    logger.info("Buscando turno funcionário...")
    try:
        table = dbf.Table("./data/horario.dbf")
        current_date = datetime.now().date()
        current_weekday = int(current_date.strftime("%w")) + 1
        with table:
            procod_idx = table.create_index(
                lambda rec: (rec.EMPR, rec.CODFUN, rec.NUMDIA, rec.ANOMES)
            )

            match = procod_idx.search(
                match=(codigo_empresa, codigo_funcionario, current_weekday, datetime.now().strftime("%Y%M"))
            )

            if len(match) == 0:
                return [0, 0, 0, 0]

            row = match[0]

            return [
                row["HORA_INI"],
                row["HORA_NIN1"],
                row["HORA_INI3"],
                row["HORA_INI4"],
            ]
    except:
        return [0, 0, 0, 0]
