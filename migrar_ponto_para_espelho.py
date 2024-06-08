from datetime import datetime, timedelta

from dateutil import parser
from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session

from configs.logger import logger

engine = create_engine("sqlite:///app.db", echo=False)

with Session(engine) as session:
    stmt = text(
        "select id, codigo_empresa, codigo_funcionario, data_ponto from ponto where strftime('%Y-%m-%d', data_ponto) between '2023-03-01' and '2023-03-31'")
    ponto = session.execute(stmt)
    ponto = ponto.all()
    logger.info(f"[{datetime.now()}] Iniciando o processamento de {len(ponto)} pontos...")

    for row in ponto:
        row_mapping = row._mapping
        data_ponto = parser.parse(row_mapping['data_ponto'])
        codigo_empresa = row_mapping['codigo_empresa']
        codigo_funcionario = row_mapping['codigo_funcionario']

        data = data_ponto.date()
        data_anterior = data - timedelta(days=1)

        start = datetime.now()

        logger.info(f"[{start}] [{codigo_empresa}{codigo_funcionario}] Iniciando o processamento do ponto...")

        stmt = text(
            f"select * from espelho where data_ponto = strftime('%Y-%m-%d', '{data_ponto}') and codigo_funcionario = {codigo_funcionario} and codigo_empresa = {codigo_empresa}")
        escala = session.execute(stmt)
        match1 = escala.first()

        resultados = []
        if match1 is not None:
            resultados = [match1]

        stmt = text(
            f"select * from espelho where data_ponto = strftime('%Y-%m-%d', '{data_anterior}') and codigo_funcionario = {codigo_funcionario} and codigo_empresa = {codigo_empresa}")
        escala = session.execute(stmt)
        match2 = escala.first()
        if match2 is not None:
            resultados = resultados + [match2]

        logger.info(f"[{datetime.now()}] Pontos localizados: {len(resultados)}")

        data_referencia = None
        data_consulta = None
        coluna_referencia = None

        for r in resultados:

            r_mapping = r._mapping

            coluna = "hora_inicial"

            if r_mapping["intervalo_inicial"] is not None:
                if abs(parser.parse(r_mapping["intervalo_inicial"]) - data_ponto) < abs(
                        parser.parse(r_mapping[coluna]) - data_ponto):
                    coluna = "intervalo_inicial"

            if r_mapping["intervalo_final"] is not None:
                if abs(parser.parse(r_mapping["intervalo_final"]) - data_ponto) < abs(
                        parser.parse(r_mapping[coluna]) - data_ponto):
                    coluna = "intervalo_final"

            if r_mapping["hora_final"] is not None:
                if abs(parser.parse(r_mapping["hora_final"]) - data_ponto) < abs(
                        parser.parse(r_mapping[coluna]) - data_ponto):
                    coluna = "hora_final"

            if data_referencia is None:
                data_referencia = r_mapping[coluna]
                data_consulta = data
                coluna_referencia = coluna
            elif r_mapping[coluna] is not None:
                if abs(parser.parse(r_mapping[coluna]) - data_ponto) < abs(parser.parse(data_referencia) - data_ponto):
                    data_referencia = r_mapping[coluna]
                    data_consulta = data_anterior
                    coluna_referencia = coluna

        if data_consulta is not None:
            stmt = text(
                f"select * from espelho where data_ponto = strftime('%Y-%m-%d', '{data_consulta}') and codigo_funcionario = {codigo_funcionario} and codigo_empresa = {codigo_empresa}")
            escala = session.execute(stmt)
            match = escala.first()

            if match is not None:
                logger.info(
                    f"[{data_ponto}] [{codigo_empresa}{codigo_funcionario}] [{coluna_referencia}] [{match._mapping['id']}] Registrando ponto espelho...")
                rec = match[0]

                if coluna_referencia == "hora_inicial":
                    stmt = text("update espelho set ponto1 = :ponto1 where id = :id")
                    session.execute(stmt, {"ponto1": data_ponto, "id": match._mapping['id']})
                elif coluna_referencia == "intervalo_inicial":
                    stmt = text("update espelho set ponto2 = :ponto2 where id = :id")
                    session.execute(stmt, {"ponto2": data_ponto, "id": match._mapping['id']})
                elif coluna_referencia == "intervalo_final":
                    stmt = text("update espelho set ponto3 = :ponto3 where id = :id")
                    session.execute(stmt, {"ponto3": data_ponto, "id": match._mapping['id']})
                elif coluna_referencia == "hora_final":
                    stmt = text("update espelho set ponto4 = :ponto4 where id = :id")
                    session.execute(stmt, {"ponto4": data_ponto, "id": match._mapping['id']})

                session.commit()
