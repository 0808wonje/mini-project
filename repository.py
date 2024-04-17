import pandas as pd
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from tqdm import trange
import ssl
from bs4 import BeautifulSoup as bs

import model
from case import Case
import parse

from sqlalchemy.orm import Session
from database import SessionLocal
import parse


ssl._create_default_https_context = ssl._create_unverified_context

db = SessionLocal()

user_id = 'wonje.j1996'
url = f'https://www.law.go.kr/DRF/lawSearch.do?OC={user_id}&target=prec&type=XML&query=%EB%8B%B4%EB%B3%B4%EA%B6%8C'


def get_xml_by_open_api(url):
    case_list = []
    response = urlopen(url).read()
    # print(response)
    xml_data = ET.fromstring(response)

    totalCnt = int(xml_data.find('totalCnt').text)
    # print(totalCnt)

    page = 1
    rows = []

    for i in trange(int(totalCnt / 20)):
        try:
            prec_info = xml_data[5:]
        except:
            break
            
        for info in prec_info:
            judicPrecNum = info.find('판례일련번호').text
            case = info.find('사건명').text
            caseNum = info.find('사건번호').text
            sentence_date = info.find('선고일자').text
            court = info.find('법원명').text
            caseInfo = info.find('사건종류명').text
            caseCode = info.find('사건종류코드').text
            judgment = info.find('판결유형').text
            sentence = info.find('선고').text
            judicPrecLink = info.find('판례상세링크').text

            rows.append({'판례일련번호': judicPrecNum,
                        '사건명': case,
                        '사건번호': caseNum,
                        '선고일자': sentence_date,
                        '법원명': court,
                        '사건종류명': caseInfo,
                        '사건종류코드': caseCode,
                        '판결유형': judgment,
                        '선고': sentence,
                        '판례상세링크': judicPrecLink})
            
            case_list.append(
                Case(title=case,
                    case_number=caseNum,
                    content=sentence,
                    vector=model.getSimilarity(sentence),
                    link=judicPrecLink)
                    )

        page += 1
        response = urlopen(url + '&page=' + str(page)).read()
        xml_data = ET.fromstring(response)


    judicPrecList = pd.DataFrame(rows)
    judicPrecList.to_csv('./judicial_precedent_list.csv', index=False)
    return case_list


def add_case(case: Case, db: Session):
    db.add(case)


def fetch_data(db: Session):
    return db.query(Case).all()


# 더미 데이터 넣는 로직
# case_list = parse.get_case_list()
# for e in case_list:
#     add_case(e, db)
# db.commit()



# for i in range(5):
#     add_case(Case(title='aaa', case_number='ffds', content='dsa', vector=v, similar_case={'vector': v}, cur_idx=13, link='sdfds'), db)
# db.commit()

# find = db.query(case.Case).filter(case.Case.id == 10).first()
# print('find_id =', find.id)
# print('find_vector =', find.similar_case['vector'])