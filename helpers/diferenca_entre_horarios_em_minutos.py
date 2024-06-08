from datetime import datetime


def diferenca_entre_horarios_em_minutos(
    data_inicial: datetime, data_final: datetime
) -> int:
    return int((data_final - data_inicial).total_seconds() / 60)
