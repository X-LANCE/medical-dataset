import random
from dataclasses import dataclass
from datetime import timedelta
from utils import generate_datetime, generate_region, str_to_date, str_to_datetime, connect_database, update_database
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


@dataclass
class mzjzjlb:
    YLJGDM: str = ''
    JZLSH: str = ''
    KH: str = ''
    KLX: int = 0
    ZSEBZ: int = 0
    JZZTDM: int = 0
    JZZTMC: str = ''
    JZJSSJ: str = ''
    TXBZ: int = 0
    ZZBZ: int = 0
    WDBZ: int = 0
    JZKSBM: str = ''
    JZKSMC: str = ''
    JZKSRQ: str = ''
    ZZYSGH: str = ''
    QTJZYSGH: str = ''
    JZZDBM: str = ''
    JZZDSM: str = ''
    MZZYZDZZBM: str = ''
    MZZYZDZZMC: str = ''
    SG: float = 0
    TZ: float = 0
    TW: float = 0
    SSY: int = 0
    SZY: int = 0
    XL: int = 0
    HXPLC: int = 0
    ML: int = 0
    JLSJ: str = ''


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


def generate_mzjzjlb(value_sets, data_hz_info):
    data = []
    for i in range(len(value_sets['门诊就诊流水号']) + len(value_sets['门诊就诊流水号或住院就诊流水号']) // 2):
        j = random.randint(0, len(data_hz_info) - 1)
        record = mzjzjlb()
        record.YLJGDM = data_hz_info[j].YLJGDM
        record.JZLSH = value_sets['门诊就诊流水号'][i] if i < len(value_sets['门诊就诊流水号']) else value_sets['门诊就诊流水号或住院就诊流水号'][i - len(value_sets['门诊就诊流水号'])]
        record.KH = data_hz_info[j].KH
        record.KLX = data_hz_info[j].KLX
        record.ZSEBZ = 0 if random.randint(0, 9) < 9 else 1
        record.JZZTDM = 0
        record.JZZTMC = '正常'
        record.JZJSSJ = generate_datetime()
        record.TXBZ = 0 if random.randint(0, 9) < 9 else 1
        record.ZZBZ = 0 if random.randint(0, 9) < 9 else 1
        record.WDBZ = 0 if random.randint(0, 9) < 9 else 1
        record.JZKSBM = random.choice(value_sets['科室编码'])
        record.JZKSMC = random.choice(value_sets['科室名称'])
        record.JZKSRQ = str(str_to_date(record.JZJSSJ[:10]) - timedelta(days=random.randint(0, 1)))
        record.ZZYSGH = random.choice(value_sets['医生工号'])
        record.QTJZYSGH = '['
        for _ in range(random.randint(0, 3)):
            record.QTJZYSGH += f"{random.choice(value_sets['医生工号'])}, "
        if record.QTJZYSGH != '[':
            record.QTJZYSGH = record.QTJZYSGH[:-2]
        record.QTJZYSGH += ']'
        record.JZZDBM = record.MZZYZDZZBM = random.choice(value_sets['疾病编码'])
        record.JZZDSM = record.MZZYZDZZMC = random.choice(value_sets['疾病名称'])
        record.SG = round(random.uniform(140, 200) if record.ZSEBZ == 0 else random.uniform(45, 55), 1)
        record.TZ = round((record.SG / 100) ** 2 * 21 + random.uniform(-3, 3) if record.ZSEBZ == 0 else (record.SG / 100) ** 2 * 12 + random.uniform(-0.3, 0.3), 1)
        record.TW = round(random.uniform(36.5, 37.5) if random.randint(0, 9) < 9 else random.uniform(37.5, 39.5), 1)
        if random.randint(0, 9) < 7:
            record.SSY = random.randint(90, 119)
            record.SZY = random.randint(60, 79)
        elif random.randint(0, 2) < 2:
            record.SSY = random.randint(120, 139)
            record.SZY = random.randint(80, 89)
        else:
            record.SSY = random.randint(140, 199)
            record.SZY = random.randint(90, 109)
        record.XL = record.ML = random.randint(55, 105)
        record.HXPLC = round(record.XL / random.uniform(4, 5))
        while 1:
            record.JLSJ = str(str_to_datetime(record.JZJSSJ) - timedelta(hours=random.randint(0, 1), minutes=random.randint(0, 59), seconds=random.randint(0, 59)))
            if record.JLSJ[:10] >= record.JZKSRQ:
                break
        data.append(record)
    return data


def generate_yiliao(value_sets):
    data_person_info = generate_person_info(value_sets)
    data_hz_info = generate_hz_info(value_sets, data_person_info)
    data_mzjzjlb = generate_mzjzjlb(value_sets, data_hz_info)
    database, cursor = connect_database('yiliao')
    update_database(database, cursor, 'person_info', data_person_info)
    update_database(database, cursor, 'hz_info', data_hz_info)
