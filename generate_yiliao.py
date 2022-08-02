import random
from dataclasses import dataclass
from utils import generate_region, connect_database, update_database
from xeger import Xeger


@dataclass
class person_info:
    RYBH: str = ''
    XM: str = ''
    JGDM: str = ''
    JGMC: str = ''


@dataclass
class hz_info:
    KH: str = ''
    KLX: int = 0
    YLJGDM: str = ''
    RYBH: str = ''


def generate_person_info(value_sets):
    data = []
    for i in range(len(value_sets['人员ID'])):
        record = person_info()
        record.RYBH = value_sets['人员ID'][i]
        record.XM = random.choice(value_sets['人员姓名'])
        record.JGDM, record.JGMC = generate_region()
        data.append(record)
    return data


def generate_hz_info(value_sets, data_person_info):
    data = []
    for i in range(len(data_person_info) * 10):
        j = random.randint(0, len(data_person_info) - 1)
        record = hz_info()
        record.KH = Xeger().xeger(r'\d{7}')
        record.KLX = random.randint(0, 2)
        record.YLJGDM = random.choice(value_sets['医疗机构代码'])
        record.RYBH = data_person_info[j].RYBH
        data.append(record)
    return data


def generate_yiliao(value_sets):
    data_person_info = generate_person_info(value_sets)
    data_hz_info = generate_hz_info(value_sets, data_person_info)
    database, cursor = connect_database('yiliao')
    update_database(database, cursor, 'person_info', data_person_info)
    update_database(database, cursor, 'hz_info', data_hz_info)
