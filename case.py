from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, Integer, JSON, String, Text
import database

# 베이스 클래스 선언
Base = declarative_base() 

# 엔티티 정의
class Case(Base):
    __tablename__ = 'sentence'

    id = Column(Integer, primary_key=True) 
    title = Column(Text) # 사건명
    case_number = Column(String(30)) # 사건번호 
    content = Column(Text) # 판결내용
    vector = Column(Text) # 벡터값
    similar_case = Column(JSON) # ??
    cur_idx = Column(Integer) # ??
    link = Column(String(200)) # ??


# 테이블 생성
Base.metadata.create_all(bind=database.engine)

