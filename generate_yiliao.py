import random
from dataclasses import dataclass
from datetime import timedelta
from generate_dataset import generate_name
from string import ascii_uppercase
from utils import generate_datetime, generate_region, generate_medical_index, str_to_date, str_to_datetime, connect_database, update_database
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


@dataclass
class zyjzjlb:
    YLJGDM: str = ''
    JZLSH: str = ''
    KH: str = ''
    KLX: int = 0
    WDBZ: int = 0
    RYDJSJ: str = ''
    RYTJDM: int = 0
    RYTJMC: str = ''
    JZKSDM: str = ''
    JZKSMC: str = ''
    RZBQDM: str = ''
    RZBQMC: str = ''
    RYCWH: str = ''
    CYKSDM: str = ''
    CYKSMC: str = ''
    CYBQDM: str = ''
    CYBQMC: str = ''
    CYCWH: str = ''
    ZYBMLX: int = 0
    ZYZDBM: str = ''
    ZYZDMC: str = ''
    ZYZYZDZZBM: str = ''
    ZYZYZDZZMC: str = ''
    MZBMLX: int = 0
    MZZDBM: str = ''
    MZZDMC: str = ''
    MZZYZDZZBM: str = ''
    RYSJ: str = ''
    CYSJ: str = ''
    CYZTDM: int = 0


@dataclass
class jybgb:
    YLJGDM: str = ''
    BGDH: str = ''
    BGRQ: str = ''
    JYLX: int = 0
    JZLSH: str = ''
    JZLX: int = 0
    KSBM: str = ''
    KSMC: str = ''
    SQRGH: str = ''
    SQRXM: str = ''
    BGRGH: str = ''
    BGRXM: str = ''
    SHRGH: str = ''
    SHRXM: str = ''
    SHSJ: str = ''
    SQKS: str = ''
    SQKSMC: str = ''
    JYKSBM: str = ''
    JYKSMC: str = ''
    BGJGDM: str = ''
    BGJGMC: str = ''
    BBDM: str = ''
    BBMC: str = ''
    BBZT: int = 0
    BBCJBW: str = ''
    JYXMMC: str = ''
    JYXMDM: str = ''
    JYSQJGMC: str = ''
    JYJGMC: str = ''
    JYJSQM: str = ''
    JYJSGH: str = ''


@dataclass
class jyjgzbb:
    JYZBLSH: str = ''
    YLJGDM: str = ''
    BGDH: str = ''
    JYRQ: str = ''
    JCRGH: str = ''
    JCRXM: str = ''
    SHRGH: str = ''
    SHRXM: str = ''
    JCXMMC: str = ''
    JCZBDM: str = ''
    JCFF: str = ''
    JCZBMC: str = ''
    JCZBJGDX: str = ''
    JCZBJGDL: float = 0
    JCZBJGDW: str = ''
    SBBM: str = ''
    YQBH: str = ''
    YQMC: str = ''
    CKZFWDX: str = ''
    CKZFWXX: float = 0
    CKZFWSX: float = 0


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
    for _ in range(len(data_person_info) * 2):
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
    for i in range(len(data_hz_info) * 2):
        j = random.randint(0, len(data_hz_info) - 1)
        record = mzjzjlb()
        record.YLJGDM = data_hz_info[j].YLJGDM
        if i < len(value_sets['门诊就诊流水号']):
            record.JZLSH = value_sets['门诊就诊流水号'][i]
        elif i < len(value_sets['门诊就诊流水号']) + len(value_sets['门诊就诊流水号或住院就诊流水号']) // 2:
            record.JZLSH = value_sets['门诊就诊流水号或住院就诊流水号'][i - len(value_sets['门诊就诊流水号'])]
        else:
            record.JZLSH = Xeger().xeger(r'\d{11}')
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


def generate_zyjzjlb(value_sets, data_hz_info):
    data = []
    for i in range(len(data_hz_info) * 2):
        j = random.randint(0, len(data_hz_info) - 1)
        record = zyjzjlb()
        record.YLJGDM = data_hz_info[j].YLJGDM
        if i < len(value_sets['住院就诊流水号']):
            record.JZLSH = value_sets['住院就诊流水号'][i]
        elif i < len(value_sets['住院就诊流水号']) + len(value_sets['门诊就诊流水号或住院就诊流水号']) // 2:
            record.JZLSH = value_sets['门诊就诊流水号或住院就诊流水号'][i - len(value_sets['住院就诊流水号']) + len(value_sets['门诊就诊流水号或住院就诊流水号']) // 2]
        else:
            record.JZLSH = Xeger().xeger(r'\d{11}')
        record.KH = data_hz_info[j].KH
        record.KLX = data_hz_info[j].KLX
        record.WDBZ = 0 if random.randint(0, 9) < 9 else 1
        record.RYDJSJ = record.RYSJ = generate_datetime()
        record.RYTJDM = random.randint(0, 2)
        if record.RYTJDM == 0:
            record.RYTJMC = '门急诊入院'
        elif record.RYTJDM == 1:
            record.RYTJMC = '转诊入院'
        else:
            record.RYTJMC = '其他'
        record.JZKSDM = random.choice(value_sets['科室编码'])
        record.JZKSMC = random.choice(value_sets['科室名称'])
        record.RZBQDM = random.choice(ascii_uppercase)
        record.RZBQMC = record.RZBQDM + '区'
        record.RYCWH = Xeger().xeger(r'\d{2}')
        if random.randint(0, 9) < 9:
            record.CYKSDM = record.JZKSDM
            record.CYKSMC = record.JZKSMC
        else:
            record.CYKSDM = random.choice(value_sets['科室编码'])
            record.CYKSMC = random.choice(value_sets['科室名称'])
        if random.randint(0, 9) < 9:
            record.CYBQDM = record.RZBQDM
            record.CYBQMC = record.RZBQMC
            record.CYCWH = record.RYCWH
        else:
            record.CYBQDM = random.choice(ascii_uppercase)
            record.CYBQMC = record.CYBQDM + '区'
            record.CYCWH = Xeger().xeger(r'\d{2}')
        record.ZYBMLX = record.MZBMLX = 0
        record.ZYZDBM = record.ZYZYZDZZBM = record.MZZDBM = record.MZZYZDZZBM = random.choice(value_sets['疾病编码'])
        record.ZYZDMC = record.ZYZYZDZZMC = record.MZZDMC = random.choice(value_sets['疾病名称'])
        record.CYSJ = str(str_to_datetime(record.RYSJ) + timedelta(days=random.randint(1, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59)))
        record.CYZTDM = 0
        data.append(record)
    return data


def generate_jybgb(value_sets, data_mzjzjlb, data_zyjzjlb):
    data = []
    for i in range((len(data_mzjzjlb) + len(data_zyjzjlb)) * 2):
        record = jybgb()
        record.JZLX = random.randint(0, 1)
        j = random.randint(0, (len(data_mzjzjlb) if record.JZLX == 0 else len(data_zyjzjlb)) - 1)
        record.YLJGDM = record.BGJGDM = data_mzjzjlb[j].YLJGDM if record.JZLX == 0 else data_zyjzjlb[j].YLJGDM
        record.BGDH = value_sets['检验报告单号'][i] if i < len(value_sets['检验报告单号']) else Xeger().xeger(r'\d{11}')
        if record.JZLX == 0:
            record.BGRQ = data_mzjzjlb[j].JZJSSJ[:10]
        else:
            while 1:
                record.BGRQ = str(str_to_datetime(data_zyjzjlb[j].RYSJ) + timedelta(days=random.randint(0, 30)))[:10]
                if record.BGRQ <= data_zyjzjlb[j].CYSJ[:10]:
                    break
        record.JYLX = 0
        record.JZLSH = data_mzjzjlb[j].JZLSH if record.JZLX == 0 else data_zyjzjlb[j].JZLSH
        record.KSBM = record.SQKS = record.JYKSBM = random.choice(value_sets['科室编码'])
        record.KSMC = record.SQKSMC = record.JYKSMC = random.choice(value_sets['科室名称'])
        record.SQRGH = Xeger().xeger(r'\d{8}')
        record.SQRXM = generate_name()[0]
        record.BGRGH = Xeger().xeger(r'\d{8}')
        record.BGRXM = generate_name()[0]
        record.SHRGH = Xeger().xeger(r'\d{8}')
        record.SHRXM = generate_name()[0]
        record.SHSJ = f'{record.BGRQ} {str(random.randint(0, 23)).zfill(2)}:{str(random.randint(0, 59)).zfill(2)}:{str(random.randint(0, 59)).zfill(2)}'
        record.BGJGMC = record.JYSQJGMC = record.JYJGMC = f"{generate_region()[1]}第{random.choice(['一', '二', '三'])}人民医院"
        record.BBDM = Xeger().xeger(r'\d{11}')
        record.JYXMMC = random.choice(['肝功能', '肾功能', '糖代谢', '血脂', '心肌酶', '离子类', '风湿三项', '特定蛋白', '铁代谢',
            '尿蛋白', '治疗药物检测', '肿瘤标志物', '甲状腺', '激素', '产筛', '心肌', '传染病', '骨标志物', '贫血', '脓毒血症', '类风关'])
        record.BBMC = record.JYXMMC + '标本'
        record.BBZT = 0
        record.BBCJBW = random.choice(value_sets['部位'])
        record.JYXMDM = Xeger().xeger(r'\d{6}')
        record.JYJSQM = generate_name()[0]
        record.JYJSGH = Xeger().xeger(r'\d{8}')
        data.append(record)
    return data


def generate_jyjgzbb(value_sets, data_jybgb):
    data = []
    for i in range(len(data_jybgb) * 2):
        j = random.randint(0, len(data_jybgb) - 1)
        record = jyjgzbb()
        record.JYZBLSH = value_sets['检验指标流水号'][i] if i < len(value_sets['检验指标流水号']) else Xeger().xeger(r'\d{11}')
        record.YLJGDM = data_jybgb[j].YLJGDM
        record.BGDH = data_jybgb[j].BGDH
        record.JYRQ = data_jybgb[j].BGRQ
        record.JCRGH = random.choice(value_sets['检测人工号'])
        record.JCRXM = random.choice(value_sets['检测人姓名'])
        record.SHRGH = Xeger().xeger(r'\d{8}')
        record.SHRXM = generate_name()[0]
        record.JCXMMC = data_jybgb[j].JYXMMC
        record.JCZBDM = random.choice(value_sets['检测指标代码'])
        record.JCZBMC, record.JCFF, record.JCZBJGDW, record.CKZFWXX, record.CKZFWSX = generate_medical_index(record.JCXMMC)
        if random.randint(0, 1) == 0:
            record.JCZBJGDX = '正常'
            record.JCZBJGDL = round(random.uniform(record.CKZFWXX, record.CKZFWSX), 2)
        else:
            record.JCZBJGDX = '异常'
            if record.CKZFWXX > 0 and random.randint(0, 1) == 0:
                while record.JCZBJGDL <= 0:
                    record.JCZBJGDL = round(record.CKZFWXX - random.uniform(0, (record.CKZFWSX - record.CKZFWXX) / 10), 2)
            else:
                record.JCZBJGDL = round(record.CKZFWSX + random.uniform(0, (record.CKZFWSX - record.CKZFWXX) / 10), 2)
        record.SBBM = Xeger().xeger(r'\d{6}')
        record.YQBH = Xeger().xeger(r'\d{6}')
        record.YQMC = '仪器' + record.YQBH
        record.CKZFWDX = f'{record.CKZFWXX}-{record.CKZFWSX} {record.JCZBJGDW}'
        data.append(record)
    return data


def generate_yiliao(value_sets):
    data_person_info = generate_person_info(value_sets)
    data_hz_info = generate_hz_info(value_sets, data_person_info)
    data_mzjzjlb = generate_mzjzjlb(value_sets, data_hz_info)
    data_zyjzjlb = generate_zyjzjlb(value_sets, data_hz_info)
    data_jybgb = generate_jybgb(value_sets, data_mzjzjlb, data_zyjzjlb)
    data_jyjgzbb = generate_jyjgzbb(value_sets, data_jybgb)
    database, cursor = connect_database('yiliao')
    update_database(database, cursor, 'person_info', data_person_info)
    update_database(database, cursor, 'hz_info', data_hz_info)
    update_database(database, cursor, 'mzjzjlb', data_mzjzjlb)
    update_database(database, cursor, 'zyjzjlb', data_zyjzjlb)
    update_database(database, cursor, 'jybgb', data_jybgb)
    update_database(database, cursor, 'jyjgzbb', data_jyjgzbb)
