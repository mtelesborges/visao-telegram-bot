import csv
import dbf
from dateutil import parser

espelho = dbf.Table('./data/ponto.dbf')

with espelho:
    idx = espelho.create_index(
        lambda rec: (rec.EMPR, rec.CODFUN)
    )

    match1 = idx.search(
        match=(409, 27)
    )

    print(len(match1))

    with open('GFG', 'w') as f:
      
        # using csv.writer method from CSV package
        write = csv.writer(f)

        write.writerows(match1)
