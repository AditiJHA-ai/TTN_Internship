from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

db_url = URL.create(
	drivername="postgresql+psycopg2",
	username="postgres",
	password="Aditijha@1104",
	host="localhost",
	port=5432,
	database="telusko",
)
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal