import dbf

db = dbf.Table("./data/ponto.dbf")
with db:
    db.add_fields("DSFOTO C(150)")
