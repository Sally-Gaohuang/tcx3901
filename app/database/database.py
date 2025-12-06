from sqlmodel import SQLModel, create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@mysql:3306/insurance")

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Debug mode
)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

