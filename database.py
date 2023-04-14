from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLITE3 CONFIG START
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SQLITE3 CONFIG END


# POSTGRES CONFIG START
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Test12345@localhost/TodoApplicationDatabase"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
# POSTGRES CONFIG END

# MYSQL CONFIG START
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Bohdan2328%40@127.0.0.1:3306/todoapp"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )
# MYSQL CONFIG END

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

