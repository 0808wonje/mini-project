from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import db_env


DB_URL = f'mysql+pymysql://{db_env.user}:{db_env.password}@{db_env.host}:3306/{db_env.db_name}'

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)