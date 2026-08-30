from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "mysql+pymysql://root:root123456@127.0.0.1:3306/fastapi_db"
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=True,
    autocommit = False
)