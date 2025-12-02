from sqlmodel import SQLModel, create_engine

DATABASE_URL = "postgresql://postgres:postgres@db:5432/authdb"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
