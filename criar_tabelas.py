from datetime import datetime

from sqlalchemy import MetaData, Text, String
from sqlalchemy import Table, Column, Integer, DateTime, Date
from sqlalchemy import create_engine

metadata_obj = MetaData()

engine = create_engine("sqlite:///app.db", echo=True)

ponto = Table(
    "ponto",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("codigo_empresa", Integer, nullable=False),
    Column("codigo_funcionario", Integer, nullable=False),
    Column("data_ponto", DateTime, nullable=False, default=datetime.now()),
    Column("endereco_ponto", Text),
    Column("observacao", Text),
    Column("foto", String),
)

espelho = Table(
    "espelho",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("codigo_empresa", Integer, nullable=False),
    Column("codigo_funcionario", Integer, nullable=False),
    Column("data_ponto", Date, nullable=False),
    Column("ponto1", DateTime),
    Column("ponto2", DateTime),
    Column("ponto3", DateTime),
    Column("ponto4", DateTime),
    Column("hora_inicial", DateTime),
    Column("intervalo_inicial", DateTime),
    Column("intervalo_final", DateTime),
    Column("hora_final", DateTime),
)

metadata_obj.create_all(engine)
