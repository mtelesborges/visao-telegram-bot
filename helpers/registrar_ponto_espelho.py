import dbf
from datetime import datetime, timedelta
from configs.logger import logger


def registrar_ponto_espelho(codigo_empresa: int, codigo_funcionario: int, data_ponto: datetime) -> None:

    try:
        logger.info(f"Registrando ponto espelho: {codigo_empresa}{codigo_funcionario}, data_ponto: {data_ponto}")
        data =  data_ponto.date()
        data_anterior = data - timedelta(days=1)

        table = dbf.Table("./data/espelho.dbf")

        with table:
            procod_idx = table.create_index(
                lambda rec: (rec.EMPR, rec.CODFUN, rec.DT_PONTO)
            )

            match1 = procod_idx.search(
                match=(codigo_empresa, codigo_funcionario, data)
            )

            resultados = match1

            match2 = procod_idx.search(
                match=(codigo_empresa, codigo_funcionario, data_anterior)
            )

            resultados = resultados + match2

            data_referencia = None
            data_consulta = None
            coluna_referencia = None

            for r in resultados:

                coluna = "HORAINI"

                if r["INTEINI"] is not None:
                    if abs(r["INTEINI"] - data_ponto) < abs(r[coluna] - data_ponto):
                        coluna = "INTEINI"

                if r["INTEFIM"] is not None:
                    if abs(r["INTEFIM"] - data_ponto) < abs(r[coluna] - data_ponto):
                        coluna = "INTEFIM"

                if r["HORAFIM"] is not None:
                    if abs(r["HORAFIM"] - data_ponto) < abs(r[coluna] - data_ponto):
                        coluna = "HORAFIM"

                if data_referencia is None:
                    data_referencia = r[coluna]
                    data_consulta = data
                    coluna_referencia = coluna
                elif abs(r[coluna] - data_ponto) < abs(data_referencia - data_ponto):
                    data_referencia = r[coluna]
                    data_consulta = data_anterior
                    coluna_referencia = coluna

            logger.info(f"Registrando ponto espelho: {codigo_empresa}{codigo_funcionario}, data_referencia: {data_referencia}, data_consulta: {data_referencia}, coluna_referencia: {coluna_referencia}")

            if data_consulta is not None:
                match = procod_idx.search(
                    match=(codigo_empresa, codigo_funcionario, data_consulta)
                )

                if len(match) == 1:
                    logger.info(f"Registrando ponto espelho: {codigo_empresa}{codigo_funcionario}, atualizando tabela...")
                    rec = match[0]

                    if coluna_referencia == "HORAINI":
                        dbf.write(rec, M_PONTO1=data_ponto)
                    elif coluna_referencia == "INTEINI":
                        dbf.write(rec, M_PONTO2=data_ponto)
                    elif coluna_referencia == "INTEFIM":
                        dbf.write(rec, M_PONTO3=data_ponto)
                    elif coluna_referencia == "HORAFIM":
                        dbf.write(rec, M_PONTO4=data_ponto)
    except Exception as e:
        logger.error(f"Registrando ponto espelho: {codigo_empresa}{codigo_funcionario}, {e}")