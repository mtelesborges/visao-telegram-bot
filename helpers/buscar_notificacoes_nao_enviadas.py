import dbf
from typing import Dict
from dateutil import parser
from datetime import datetime


def buscar_notificacoes_nao_enviadas(
    codigo_empresa: int, codigo_funcionario: int
) -> Dict:
    table = dbf.Table("./data/notificacoes.dbf")
    with table:
        procod_idx = table.create_index(
            lambda rec: (rec.EMPR, rec.CODFUN, rec.ENVIADA)
        )
        match = procod_idx.search(
            match=(codigo_empresa, codigo_funcionario, 0)
        )

        if len(match) == 0:
            return []

        notificacoes = []

        for item in match:
            data_notificacao = item["DTNOTIFIC"]
            if parser.parse(data_notificacao) < datetime.now():
                notificacoes.append(item["DSNOTIFIC"])

        return notificacoes
