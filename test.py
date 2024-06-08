import dbf
from sqlalchemy.orm import Session
from sqlalchemy import text, create_engine
from dateutil import parser
from configs.logger import logger

engine = create_engine("sqlite:///app.db", echo=True)

espelho = dbf.Table('./data/espelho.dbf')

with Session(engine) as session:
    stmt = text("select * from espelho")
    result = session.execute(stmt)
    result = result.all()

    for row in result:
        row_mapping = row._mapping

        with espelho:
            idx = espelho.create_index(
                lambda rec: (rec.EMPR, rec.CODFUN, rec.DT_PONTO)
            )

            match1 = idx.search(
                match=(row_mapping['codigo_empresa'], row_mapping['codigo_funcionario'], parser.parse(row_mapping['data_ponto']).date())
            )

            if len(match1) == 1:
                logger.info(f'[Ponto migrado] {row_mapping}')
                rec=match1[0]
                ponto1 = parser.parse(f"{row_mapping['data_ponto']} {row_mapping['ponto1']}")
                ponto2 = parser.parse(f"{row_mapping['data_ponto']} {row_mapping['ponto2']}")
                ponto3 = parser.parse(f"{row_mapping['data_ponto']} {row_mapping['ponto3']}")
                ponto4 = parser.parse(f"{row_mapping['data_ponto']} {row_mapping['ponto4']}")
                dbf.write(rec,
                          M_PONTO1=ponto1,
                          M_PONTO2=ponto2,
                          M_PONTO3=ponto3,
                          M_PONTO4=ponto4)
            else:
                logger.info(f'[match1] {len(match1)}')


