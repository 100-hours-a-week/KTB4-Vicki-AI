from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine(
    "mysql+pymysql://kbt:0629@localhost:3306/community"\
)

Session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = Session()

    try:
        yield db
    finally:
        db.close()
