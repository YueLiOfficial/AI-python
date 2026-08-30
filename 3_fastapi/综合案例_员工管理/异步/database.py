from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(
    "mysql+aiomysql://root:root123456@127.0.0.1:3306/fastapi_db"
)

SessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=True,
    autocommit = False
)