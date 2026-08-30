from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 创建engine，连接MySQL
engine = create_engine(
    url="mysql+pymysql://root:root123456@127.0.0.1:3306/fastapi_db",
    # echo=True, # 启用日志输出，打印执行的SQL语句，方便调试，开发环境启用，生产环境关闭
    pool_pre_ping=True # 连接前检查有效性，避免连接失败
)

# 创建会话工厂，能够生成会话
SessionLocal = sessionmaker(
    bind=engine,
    autocommit = False
)