import dbf
from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///app.db", echo=True)

ponto = dbf.Table('./data/ponto.dbf')

stmt = text(
    "insert into ponto(codigo_empresa,  codigo_funcionario,  data_ponto, observacao, foto) values(:codigo_empresa,  :codigo_funcionario, :data_ponto, :observacao, :foto)")

with ponto:
    for row in ponto:
        with Session(engine) as session:
            session.execute(stmt, {"codigo_empresa": row["EMPR"], "codigo_funcionario": row["CODFUN"],
                                   "data_ponto": row["DTPONTO"], "observacao": row["OBS"], "foto": row["FOTO"]})
            session.commit()
