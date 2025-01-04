from db.base import engine
from sqlalchemy.orm import sessionmaker

session = sessionmaker(bind=engine)
