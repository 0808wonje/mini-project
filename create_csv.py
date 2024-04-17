from sqlalchemy.orm import Session
from database import SessionLocal
import parse
import case

db = SessionLocal()


def get_all_data():
    return db.query(case.Case).all()


with open ('data.txt', 'w') as data_csv:
    for e in get_all_data():
        fields = [str(e.id), e.case_number, e.title, e.content, str(e.vector), str(e.similar_case), str(e.cur_idx), e.link]
        data_csv.write(",".join(fields))
