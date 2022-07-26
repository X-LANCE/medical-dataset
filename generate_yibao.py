import random
from dataclasses import dataclass
from datetime import date
from generate_dataset import generate_date, generate_two_dates, generate_name
from xeger import Xeger


@dataclass
class t_kc21:
    MED_CLINIC_ID: str = ''
    PERSON_ID: str = ''
    PERSON_NM: str = ''
    IDENTITY_CARD: str = ''
    PERSON_SEX: int = 0
    PERSON_AGE: int = 0
    IN_HOSP_DATE: str = ''
    OUT_HOSP_DATE: str = ''
    FLX_MED_ORG_ID: str = ''
    MED_SER_ORG_NO: str = ''
    CLINIC_TYPE: int = 0
    CLINIC_ID: str = ''
    IN_DIAG_DIS_CD: str = ''
    IN_DIAG_DIS_NM: str = ''
    OUT_DIAG_DIS_CD: str = ''
    OUT_DIAG_DIS_NM: str = ''
    MED_ORG_DEPT_CD: str = ''
    MED_ORG_DEPT_NM: str = ''
    OUT_DIAG_DOC_CD: str = ''
    OUT_DIAG_DOC_NM: str = ''
    MAIN_COND_DES: str = ''
    INSU_TYPE: int = 0
    IN_HOSP_DAYS: int = 0
    MED_AMOUT: float = 0
    HOSP_STS: int = 0
    SERVANT_FLG: int = 0
    INSURED_STS: int = 0
    REMOTE_SETTLE_FLG: int = 0


@dataclass
class t_kc22:
    MED_EXP_DET_ID: str = ''
    MED_CLINIC_ID: str = ''
    SOC_SRT_DIRE_CD: str = ''
    SOC_SRT_DIRE_NM: str = ''
    DIRE_TYPE: int = 0
    CHA_ITEM_LEV: int = 0
    MED_INV_ITEM_TYPE: int = 0
    MED_DIRE_CD: str = ''
    MED_DIRE_NM: str = ''
    DOSE_FORM: str = ''
    SPEC: str = ''
    USE_FRE: str = ''
    EACH_DOSAGE: str = ''
    QTY: int = 0
    UNIVALENT: float = 0
    AMOUNT: float = 0
    SELF_PAY_PRO: float = 0
    SELF_PAY_AMO: float = 0
    UP_LIMIT_AMO: float = 0
    OVE_SELF_AMO: float = 0
    FLX_MED_ORG_ID: str = ''
    MED_ORG_DEPT_CD: str = ''
    MED_ORG_DEPT_NM: str = ''
    HOSP_DOC_CD: str = ''
    HOSP_DOC_NM: str = ''
    PRESCRIPTION_CODE: str = ''
    PRESCRIPTION_ID: str = ''
    STA_FLG: int = 0
    STA_DATE: str = ''
    REMOTE_SETTLE_FLG: int = 0


def str_to_date(string):
    return date(int(string[:4]), int(string[5:7]), int(string[8:]))


def generate_t_kc21(value_sets):
    data = []
    for i in range(len(value_sets['医疗就诊ID'])):
        record = t_kc21()
        record.MED_CLINIC_ID = value_sets['医疗就诊ID'][i]
        record.PERSON_ID = random.choice(value_sets['人员ID'])
        record.PERSON_NM = random.choice(value_sets['人员姓名'])
        record.IDENTITY_CARD = Xeger().xeger(r'\d{17}(\d|X)')
        record.PERSON_SEX = random.randint(1, 2)
        record.PERSON_AGE = random.randint(1, 100)
        record.IN_HOSP_DATE, record.OUT_HOSP_DATE = generate_two_dates()
        record.FLX_MED_ORG_ID = record.MED_SER_ORG_NO = random.choice(value_sets['医疗机构代码'])
        record.CLINIC_TYPE = random.randint(1, 4)
        record.CLINIC_ID = random.choice(value_sets['门诊就诊流水号或住院就诊流水号'])
        record.IN_DIAG_DIS_CD = record.OUT_DIAG_DIS_CD = random.choice(value_sets['疾病编码'])
        record.IN_DIAG_DIS_NM = record.OUT_DIAG_DIS_NM = random.choice(value_sets['疾病名称'])
        record.MED_ORG_DEPT_CD = random.choice(value_sets['科室编码'])
        record.MED_ORG_DEPT_NM = random.choice(value_sets['科室名称'])
        record.OUT_DIAG_DOC_CD = Xeger().xeger(r'\d{8}')
        record.OUT_DIAG_DOC_NM = generate_name()[0]
        record.MAIN_COND_DES = random.choice(['良性', '中性', '恶性'])
        record.INSU_TYPE = random.choice([0, 51])
        record.IN_HOSP_DAYS = (str_to_date(record.OUT_HOSP_DATE) - str_to_date(record.IN_HOSP_DATE)).days
        record.MED_AMOUT = round(random.uniform(0, 10000), 2)
        record.HOSP_STS = random.randint(0, 1)
        record.SERVANT_FLG = random.randint(0, 1)
        record.INSURED_STS = random.randint(0, 1)
        record.REMOTE_SETTLE_FLG = random.randint(0, 2)
        data.append(record)
    return data


def generate_t_kc22(value_sets, data_t_kc21):
    data = []
    for i in range(len(value_sets['人员医疗费用明细ID'])):
        j = random.randint(0, len(data_t_kc21) - 1)
        record = t_kc22()
        record.MED_EXP_DET_ID = value_sets['人员医疗费用明细ID'][i]
        record.MED_CLINIC_ID = data_t_kc21[j].MED_CLINIC_ID
        record.SOC_SRT_DIRE_CD = record.MED_DIRE_CD = random.choice(value_sets['社保三大目录统一编码'])
        record.SOC_SRT_DIRE_NM = record.MED_DIRE_NM = random.choice(value_sets['社保三大目录名称'])
        record.DIRE_TYPE = random.randint(0, 1)
        record.CHA_ITEM_LEV = random.randint(0, 1)
        record.MED_INV_ITEM_TYPE = random.choice([11, 21, 22, 24])
        record.DOSE_FORM = random.choice(['汤', '酒', '丸', '散', '膏', '丹', '锭', '片', '露', '霜', '胶', '茶', '曲'])
        record.SPEC = f'{random.randint(10, 50)}mg*{random.randint(10, 20)}'
        record.USE_FRE = random.choice(['每天', '日两次', '日三次'])
        record.EACH_DOSAGE = str(random.randint(1, 3))
        record.QTY = random.randint(1, 100)
        record.UNIVALENT = round(random.uniform(0, 100), 2)
        record.AMOUNT = record.QTY * record.UNIVALENT
        record.SELF_PAY_PRO = round(random.uniform(0, 1), 2)
        record.SELF_PAY_AMO = record.AMOUNT * record.SELF_PAY_PRO
        record.UP_LIMIT_AMO = round(random.uniform(0, 10000), 2)
        record.OVE_SELF_AMO = round(random.uniform(0, 10000), 2)
        record.FLX_MED_ORG_ID = data_t_kc21[j].FLX_MED_ORG_ID
        record.MED_ORG_DEPT_CD = data_t_kc21[j].MED_ORG_DEPT_CD
        record.MED_ORG_DEPT_NM = data_t_kc21[j].MED_ORG_DEPT_NM
        record.HOSP_DOC_CD = Xeger().xeger(r'\d{8}')
        record.HOSP_DOC_NM = generate_name()[0]
        record.PRESCRIPTION_CODE = Xeger().xeger(r'\d{11}')
        record.PRESCRIPTION_ID = Xeger().xeger(r'\d{11}')
        record.STA_FLG = random.randint(0, 1)
        record.STA_DATE = generate_date()[0]
        record.REMOTE_SETTLE_FLG = data_t_kc21[j].REMOTE_SETTLE_FLG
        data.append(record)
    return data


def generate_t_kc24(value_sets, data_t_kc21):
    data = []
    return data


def generate_yibao(value_sets):
    data_t_kc21 = generate_t_kc21(value_sets)
    data_t_kc22 = generate_t_kc22(value_sets, data_t_kc21)
    data_t_kc24 = generate_t_kc24(value_sets, data_t_kc21)
