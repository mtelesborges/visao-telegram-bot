from datetime import datetime

import dbf
from typing import Dict
from dateutil import parser


def burcar_horario_ultimo_ponto_funcionario(
    codigo_empresa: int, codigo_funcionario: int
) -> datetime:
    try:
        table = dbf.Table("./data/ponto.dbf")
        with table:
        
            procod_idx = table.create_index(lambda rec: (rec.EMPR, rec.CODFUN))
            match = procod_idx.search(match=(codigo_empresa, codigo_funcionario))
            if len(match) == 0:
                return None
            ponto = match[-1]
            
            return parser.parse(ponto["DTPONTO"])
    except:
        return None
