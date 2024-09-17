from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = engine = create_engine("postgresql://postgres:Shivam123@localhost:5432/Person", echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)