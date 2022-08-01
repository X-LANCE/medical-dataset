import random
from dataclasses import dataclass
from utils import generate_region, connect_database, update_database


@dataclass
class person_info:
    RYBH: str = ''
    XM: str = ''
    JGDM: str = ''
    JGMC: str = ''


def generate_person_info(value_sets):
    data = []
    for i in range(len(value_sets['人员ID'])):
        record = person_info()
        record.RYBH = value_sets['人员ID'][i]
        record.XM = random.choice(value_sets['人员姓名'])
        record.JGMC, record.JGDM = generate_region()
        data.append(record)
    return data


def generate_yiliao(value_sets):
    data_person_info = generate_person_info(value_sets)
    print(data_person_info[0])
    database, cursor = connect_database('yiliao')
    update_database(database, cursor, 'person_info', data_person_info)
