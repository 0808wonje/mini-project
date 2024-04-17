import xml.etree.ElementTree as ET
import model
from case import Case

with open ('prec.xml', 'r') as xml_file:
    xml_data = xml_file.read()

root = ET.fromstring(xml_data)


def get_case_list():
    result = []
    for serial in root.findall('prec'):
        title = serial.find('사건명').text
        case_number = serial.find('사건번호').text
        content = serial.find('판결유형').text
        vector = model.stringToVector(serial.find('사건명').text)
        similar_case = {'?' : '?'}
        cur_idx = 1
        link = serial.find('판례상세링크').text
        print(f'{case_number} : {title}')
        result.append(Case(title=title.strip(),
                        case_number=case_number,
                        content=content,
                        vector=vector,
                        similar_case=similar_case,
                        cur_idx=cur_idx,
                        link=link))
    return result
