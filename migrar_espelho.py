import dbf
from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///app.db", echo=True)

espelho = dbf.Table('./data/espelho.dbf')

stmt_insert = text(
    "insert into espelho(codigo_empresa,  codigo_funcionario,  data_ponto, hora_inicial, intervalo_inicial, intervalo_final, hora_final, ponto1, ponto2, ponto3, ponto4) values(:codigo_empresa, :codigo_funcionario, :data_ponto, :hora_inicial, :intervalo_inicial, :intervalo_final, :hora_final, :ponto1, :ponto2, :ponto3, :ponto4)")

with espelho:
    for row in espelho:
        with Session(engine) as session:
            data_ponto = row["DT_PONTO"]
            codigo_funcionario = row["CODFUN"]
            codigo_empresa = row["EMPR"]

            stmt_check_if_exists = text(
                f"select * from espelho where data_ponto = strftime('%Y-%m-%d', '{data_ponto}') and codigo_funcionario = {codigo_funcionario} and codigo_empresa = {codigo_empresa}")

            if session.execute(stmt_check_if_exists).first() is None:
                session.execute(stmt_insert, {"codigo_empresa": codigo_empresa, "codigo_funcionario": codigo_funcionario,
                                    "data_ponto": data_ponto, "hora_inicial": row["HORAINI"],
                                    "intervalo_inicial": row["INTEINI"], "intervalo_final": row["INTEFIM"],
                                    "hora_final": row["HORAFIM"], "ponto1": row["M_PONTO1"], "ponto2": row["M_PONTO2"],
                                    "ponto3": row["M_PONTO3"], "ponto4": row["M_PONTO4"]})
            session.commit()
