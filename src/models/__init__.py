from .DB import DB
db = DB("mysql+mysqlconnector://root:303@localhost/quiz")
db.create_tables()
