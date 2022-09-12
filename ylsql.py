import argparse
import json
import random
from utils import connect_database

SCHEMA_MAPPING = {
    'yibao': '医保表',
    'yiliao': '医疗表'
}

TABLE_MAPPING = {
    't_kc21': '医疗就诊表',
    't_kc22': '人员医疗费用明细表',
    't_kc24': '人员医疗保险待遇支付台账表',
    'person_info': '人员信息表',
    'hz_info': '患者信息表',
    'mzjzjlb': '门诊就诊记录表',
    'zyjzjlb': '住院就诊记录表',
    'jybgb': '检验报告表',
    'jyjgzbb': '检验结果指标表'
}

COLUMN_MAPPING = {
    ('t_kc21', 'MED_CLINIC_ID'): '医疗就诊ID',
    ('t_kc21', 'OVERALL_CD_ORG'): '统筹区编码(机构)',
    ('t_kc21', 'OVERALL_CD_PERSON'): '统筹区编码(人员)',
    ('t_kc21', 'COMP_ID'): '单位ID',
    ('t_kc21', 'PERSON_ID'): '人员ID',
    ('t_kc21', 'PERSON_NM'): '人员姓名',
    ('t_kc21', 'IDENTITY_CARD'): '公民身份号码',
    ('t_kc21', 'SOC_SRT_CARD'): '社会保障卡号',
    ('t_kc21', 'PERSON_SEX'): '人员性别',
    ('t_kc21', 'PERSON_AGE'): '人员年龄',
    ('t_kc21', 'IN_HOSP_DATE'): '入院日期',
    ('t_kc21', 'OUT_HOSP_DATE'): '出院日期',
    ('t_kc21', 'DIFF_PLACE_FLG'): '异地标志',
    ('t_kc21', 'FLX_MED_ORG_ID'): '定点医疗机构ID',
    ('t_kc21', 'MED_SER_ORG_NO'): '医疗服务机构编号',
    ('t_kc21', 'CLINIC_TYPE'): '就诊类型',
    ('t_kc21', 'MED_TYPE'): '医疗类别',
    ('t_kc21', 'CLINIC_ID'): '住院号(门诊号)',
    ('t_kc21', 'IN_DIAG_DIS_CD'): '入院诊断疾病编码',
    ('t_kc21', 'IN_DIAG_DIS_NM'): '入院诊断疾病名称',
    ('t_kc21', 'OUT_DIAG_DIS_CD'): '出院诊断疾病编码',
    ('t_kc21', 'OUT_DIAG_DIS_NM'): '出院诊断疾病名称',
    ('t_kc21', 'INPT_AREA_BED'): '病区床位',
    ('t_kc21', 'MED_ORG_DEPT_CD'): '医疗机构科室编码',
    ('t_kc21', 'MED_ORG_DEPT_NM'): '医疗机构科室名称',
    ('t_kc21', 'OUT_DIAG_DOC_CD'): '出院诊断医生编码',
    ('t_kc21', 'OUT_DIAG_DOC_NM'): '出院诊断医生姓名',
    ('t_kc21', 'MAIN_COND_DES'): '主要病情描述',
    ('t_kc21', 'INSU_TYPE'): '险种类型',
    ('t_kc21', 'IN_HOSP_DAYS'): '住院床日',
    ('t_kc21', 'MED_AMOUT'): '医疗费总额',
    ('t_kc21', 'FERTILITY_STS'): '生育状态',
    ('t_kc21', 'DATA_ID'): '批次代码',
    ('t_kc21', 'SYNC_TIME'): '同步时间',
    ('t_kc21', 'REIMBURSEMENT_FLG'): '报销标志',
    ('t_kc21', 'HOSP_LEV'): '医院等级',
    ('t_kc21', 'HOSP_STS'): '在院状态',
    ('t_kc21', 'INSURED_IDENTITY'): '个人身份',
    ('t_kc21', 'SERVANT_FLG'): '公务员标识',
    ('t_kc21', 'TRADE_TYPE'): '交易类型',
    ('t_kc21', 'INSURED_STS'): '人员状态',
    ('t_kc21', 'REMOTE_SETTLE_FLG'): '异地结算标志',
    ('t_kc22', 'MED_EXP_DET_ID'): '人员医疗费用明细ID',
    ('t_kc22', 'OVERALL_CD_ORG'): '统筹区编码(机构)',
    ('t_kc22', 'OVERALL_CD_PERSON'): '统筹区编码(人员)',
    ('t_kc22', 'MED_CLINIC_ID'): '医疗就诊ID',
    ('t_kc22', 'MED_EXP_BILL_ID'): '人员医疗费用单据ID',
    ('t_kc22', 'SOC_SRT_DIRE_CD'): '社保三大目录统一编码',
    ('t_kc22', 'SOC_SRT_DIRE_NM'): '社保三大目录名称',
    ('t_kc22', 'DIRE_TYPE'): '三大目录类别',
    ('t_kc22', 'CHA_ITEM_LEV'): '收费项目等级',
    ('t_kc22', 'MED_INV_ITEM_TYPE'): '医疗发票项目类别',
    ('t_kc22', 'MED_DIRE_CD'): '医疗机构三大目录编码',
    ('t_kc22', 'MED_DIRE_NM'): '医疗机构三大目录名称',
    ('t_kc22', 'VAL_UNIT'): '使用单位(计价单位)',
    ('t_kc22', 'DOSE_UNIT'): '剂量单位',
    ('t_kc22', 'DOSE_FORM'): '剂型',
    ('t_kc22', 'SPEC'): '规格',
    ('t_kc22', 'USE_FRE'): '使用频次',
    ('t_kc22', 'EACH_DOSAGE'): '每次用量',
    ('t_kc22', 'QTY'): '数量',
    ('t_kc22', 'UNIVALENT'): '单价',
    ('t_kc22', 'AMOUNT'): '金额',
    ('t_kc22', 'SELF_PAY_PRO'): '自付比例',
    ('t_kc22', 'RER_SOL'): '自付金额(自理)',
    ('t_kc22', 'SELF_PAY_AMO'): '自费金额',
    ('t_kc22', 'UP_LIMIT_AMO'): '定价上限金额',
    ('t_kc22', 'OVE_SELF_AMO'): '超限价自付金额',
    ('t_kc22', 'EXP_OCC_DATE'): '费用发生日期',
    ('t_kc22', 'RECIPE_BILL_ID'): '处方单据号',
    ('t_kc22', 'FLX_MED_ORG_ID'): '定点医疗机构ID',
    ('t_kc22', 'MED_ORG_DEPT_CD'): '医疗机构科室编码',
    ('t_kc22', 'MED_ORG_DEPT_NM'): '医疗机构科室名称',
    ('t_kc22', 'HOSP_DOC_CD'): '开具医师编码',
    ('t_kc22', 'HOSP_DOC_NM'): '开具医师姓名',
    ('t_kc22', 'REF_STA_FLG'): '退费结算标志',
    ('t_kc22', 'DATA_ID'): '批次代码',
    ('t_kc22', 'SYNC_TIME'): '同步时间',
    ('t_kc22', 'PRESCRIPTION_CODE'): '处方号',
    ('t_kc22', 'PRESCRIPTION_ID'): '处方流水号',
    ('t_kc22', 'TRADE_TYPE'): '交易类型',
    ('t_kc22', 'STA_FLG'): '结算标志',
    ('t_kc22', 'STA_DATE'): '结算日期',
    ('t_kc22', 'REIMBURS_TYPE'): '报销类别',
    ('t_kc22', 'FXBZ'): '分析标志',
    ('t_kc22', 'REMOTE_SETTLE_FLG'): '异地结算标志',
    ('t_kc24', 'MED_SAFE_PAY_ID'): '人员医疗保险待遇支付台账ID(单据号)',
    ('t_kc24', 'OVERALL_CD_ORG'): '统筹区编码(机构)',
    ('t_kc24', 'OVERALL_CD_PERSON'): '统筹区编码(人员)',
    ('t_kc24', 'MED_CLINIC_ID'): '医疗就诊ID',
    ('t_kc24', 'REF_SLT_FLG'): '退费结算标志',
    ('t_kc24', 'CLINIC_SLT_DATE'): '就诊结算日期',
    ('t_kc24', 'COMP_ID'): '单位ID',
    ('t_kc24', 'PERSON_ID'): '人员ID',
    ('t_kc24', 'FLX_MED_ORG_ID'): '定点医疗机构ID',
    ('t_kc24', 'INSU_TYPE'): '险种类型',
    ('t_kc24', 'MED_AMOUT'): '医疗费总额',
    ('t_kc24', 'PER_ACC_PAY'): '个人账户支出',
    ('t_kc24', 'OVE_PAY'): '统筹基金支出',
    ('t_kc24', 'ILL_PAY'): '大病支付',
    ('t_kc24', 'CIVIL_SUBSIDY'): '民政补助',
    ('t_kc24', 'PER_SOL'): '个人自理(自付)',
    ('t_kc24', 'PER_EXP'): '个人自费',
    ('t_kc24', 'DATA_ID'): '批次代码',
    ('t_kc24', 'SYNC_TIME'): '同步时间',
    ('t_kc24', 'OUT_HOSP_DATE'): '出院日期',
    ('t_kc24', 'CLINIC_ID'): '住院(门诊)流水号',
    ('t_kc24', 'MED_TYPE'): '医疗类别',
    ('t_kc24', 'INSURED_STS'): '人员状态',
    ('t_kc24', 'INSURED_IDENTITY'): '个人身份',
    ('t_kc24', 'TRADE_TYPE'): '交易类型',
    ('t_kc24', 'RECIPE_BILL_ID'): '处方单据号',
    ('t_kc24', 'ACCOUNT_DASH_DATE'): '账户冲减日期',
    ('t_kc24', 'ACCOUNT_DASH_FLG'): '账户冲减标志',
    ('t_kc24', 'REIMBURS_FLG'): '报销标志',
    ('t_kc24', 'SENDER_DEAL_ID'): '发送方(医疗机构)交易流水号',
    ('t_kc24', 'RECEIVER_DEAL_ID'): '接收方(医保中心)交易流水号',
    ('t_kc24', 'SENDER_REVOKE_ID'): '发送方(医疗机构)被撤销交易流水号',
    ('t_kc24', 'RECEIVER_REVOKE_ID'): '接收方(医保中心)被撤销交易流水号',
    ('t_kc24', 'SENDER_OFFSET_ID'): '发送方(医疗机构)被冲正交易流水号',
    ('t_kc24', 'RECEIVER_OFFSET_ID'): '接收方(医保中心)被冲正交易流水号',
    ('t_kc24', 'LAS_OVE_PAY'): '上次统筹段支付金额',
    ('t_kc24', 'OVE_ADD_PAY'): '上次可用统筹累计(即上次进入统筹累计)',
    ('t_kc24', 'SUP_ADD_PAY'): '上次补充段支付累计',
    ('t_kc24', 'CKC102'): '符合基本医疗金额',
    ('t_kc24', 'CASH_PAY'): '现金支付',
    ('t_kc24', 'COM_ACC_PAY'): '公补帐户支付',
    ('t_kc24', 'ENT_ACC_PAY'): '企补帐户支付',
    ('t_kc24', 'ENT_PAY'): '企补支付',
    ('t_kc24', 'COM_PAY'): '公补支付',
    ('t_kc24', 'OLDC_FUND_PAY'): '离休老干部基金支付',
    ('t_kc24', 'SPE_FUND_PAY'): '二等乙专项基金支付',
    ('person_info', 'RYBH'): '人员编号',
    ('person_info', 'XBDM'): '性别代码',
    ('person_info', 'XBMC'): '性别名称',
    ('person_info', 'XM'): '患者姓名',
    ('person_info', 'CSRQ'): '出生日期',
    ('person_info', 'CSD'): '出生地代码',
    ('person_info', 'MZDM'): '民族代码',
    ('person_info', 'MZMC'): '民族名称',
    ('person_info', 'GJDM'): '国籍代码',
    ('person_info', 'GJMC'): '国籍名称',
    ('person_info', 'JGDM'): '籍贯代码',
    ('person_info', 'JGMC'): '籍贯名称',
    ('person_info', 'XLDM'): '学历代码',
    ('person_info', 'XLMC'): '学历名称',
    ('person_info', 'ZYLBDM'): '职业类别代码',
    ('person_info', 'ZYMC'): '职业名称',
    ('hz_info', 'KH'): '卡号',
    ('hz_info', 'KLX'): '卡类型',
    ('hz_info', 'YLJGDM'): '医疗机构组织机构代码',
    ('hz_info', 'RYBH'): '人员编号',
    ('mzjzjlb', 'YLJGDM'): '医疗机构组织机构代码',
    ('mzjzjlb', 'JZLSH'): '门诊就诊流水号',
    ('mzjzjlb', 'KH'): '卡号',
    ('mzjzjlb', 'KLX'): '卡类型',
    ('mzjzjlb', 'MJZH'): '门(急)诊号',
    ('mzjzjlb', 'HZXM'): '患者姓名',
    ('mzjzjlb', 'NLS'): '年龄(岁)',
    ('mzjzjlb', 'NLY'): '年龄(月)',
    ('mzjzjlb', 'ZSEBZ'): '新生儿标志',
    ('mzjzjlb', 'JZZTDM'): '就诊状态代码',
    ('mzjzjlb', 'JZZTMC'): '就诊状态名称',
    ('mzjzjlb', 'JZJSSJ'): '就诊结束日期时间',
    ('mzjzjlb', 'TXBZ'): '特需标志',
    ('mzjzjlb', 'ZZBZ'): '转诊标志',
    ('mzjzjlb', 'WDBZ'): '外地标志',
    ('mzjzjlb', 'JZKSBM'): '就诊科室编码',
    ('mzjzjlb', 'JZKSMC'): '就诊科室名称',
    ('mzjzjlb', 'JZKSRQ'): '门诊就诊日期',
    ('mzjzjlb', 'ZZYSGH'): '首诊医生工号',
    ('mzjzjlb', 'QTJZYSGH'): '其他接诊医生工号列表',
    ('mzjzjlb', 'JZZDBM'): '门诊诊断编码(主要诊断)',
    ('mzjzjlb', 'JZZDSM'): '门诊诊断名称',
    ('mzjzjlb', 'MZZYZDZZBM'): '门诊中医诊断(证)编号',
    ('mzjzjlb', 'MZZYZDZZMC'): '门诊中医诊断(证)名称',
    ('mzjzjlb', 'SG'): '身高(cm)',
    ('mzjzjlb', 'TZ'): '体重',
    ('mzjzjlb', 'TW'): '体温',
    ('mzjzjlb', 'SSY'): '收缩压(mmHg)',
    ('mzjzjlb', 'SZY'): '舒张压(mmHg)',
    ('mzjzjlb', 'XL'): '心率',
    ('mzjzjlb', 'HXPLC'): '呼吸频率(次/min)',
    ('mzjzjlb', 'ML'): '脉率',
    ('mzjzjlb', 'JLSJ'): '记录日期时间',
    ('zyjzjlb', 'YLJGDM'): '医疗机构组织机构代码',
    ('zyjzjlb', 'JZLSH'): '住院就诊流水号',
    ('zyjzjlb', 'MZJZLSH'): '门诊就诊流水号',
    ('zyjzjlb', 'KH'): '卡号',
    ('zyjzjlb', 'KLX'): '卡类型',
    ('zyjzjlb', 'HZXM'): '患者姓名',
    ('zyjzjlb', 'WDBZ'): '外地标志',
    ('zyjzjlb', 'RYDJSJ'): '入院登记日期时间',
    ('zyjzjlb', 'RYTJDM'): '入院途径代码',
    ('zyjzjlb', 'RYTJMC'): '入院途径名称',
    ('zyjzjlb', 'JZKSDM'): '入院科室代码',
    ('zyjzjlb', 'JZKSMC'): '入院科室名称',
    ('zyjzjlb', 'RZBQDM'): '入住病区代码',
    ('zyjzjlb', 'RZBQMC'): '入住病区名称',
    ('zyjzjlb', 'RYCWH'): '入院床位号',
    ('zyjzjlb', 'CYKSDM'): '出院科室代码',
    ('zyjzjlb', 'CYKSMC'): '出院科室名称',
    ('zyjzjlb', 'CYBQDM'): '出院病区代码',
    ('zyjzjlb', 'CYBQMC'): '出院病区名称',
    ('zyjzjlb', 'CYCWH'): '出院床位号',
    ('zyjzjlb', 'ZYBMLX'): '住院主要诊断编码类型',
    ('zyjzjlb', 'ZYZDBM'): '住院主要诊断编码列表',
    ('zyjzjlb', 'ZYZDMC'): '住院主要诊断名称列表',
    ('zyjzjlb', 'ZYZYZDZZBM'): '住院中医诊断(证)编号',
    ('zyjzjlb', 'ZYZYZDZZMC'): '住院中医诊断(证)名称',
    ('zyjzjlb', 'MZBMLX'): '门诊主要诊断编码类型',
    ('zyjzjlb', 'MZZDBM'): '门诊主要诊断编码列表',
    ('zyjzjlb', 'MZZDMC'): '门诊主要诊断名称列表',
    ('zyjzjlb', 'MZZYZDZZBM'): '门诊中医诊断(证)编号',
    ('zyjzjlb', 'RYSJ'): '入院日期时间',
    ('zyjzjlb', 'CYSJ'): '出院日期时间',
    ('zyjzjlb', 'CYZTDM'): '出院状态代码',
    ('jybgb', 'YLJGDM'): '医疗机构组织机构代码',
    ('jybgb', 'BGDH'): '检验报告单号',
    ('jybgb', 'BGRQ'): '报告日期',
    ('jybgb', 'JYLX'): '检验类型',
    ('jybgb', 'JZLSH'): '就诊流水号',
    ('jybgb', 'JZLX'): '就诊类型',
    ('jybgb', 'KSBM'): '科室编码',
    ('jybgb', 'KSMC'): '科室名称',
    ('jybgb', 'SQRGH'): '申请人工号',
    ('jybgb', 'SQRXM'): '申请人姓名',
    ('jybgb', 'BGRGH'): '报告人工号',
    ('jybgb', 'BGRXM'): '报告人姓名',
    ('jybgb', 'SHRGH'): '审核人工号',
    ('jybgb', 'SHRXM'): '审核人姓名',
    ('jybgb', 'SHSJ'): '审核日期时间',
    ('jybgb', 'SQKS'): '申请科室编码',
    ('jybgb', 'SQKSMC'): '申请科室名称',
    ('jybgb', 'JYKSBM'): '检验科室编码',
    ('jybgb', 'JYKSMC'): '检验科室名称',
    ('jybgb', 'BGJGDM'): '报告机构代码',
    ('jybgb', 'BGJGMC'): '报告机构名称',
    ('jybgb', 'SQRQ'): '申请日期',
    ('jybgb', 'CJRQ'): '采集日期',
    ('jybgb', 'JYRQ'): '检验日期',
    ('jybgb', 'BGSJ'): '报告日期时间',
    ('jybgb', 'BBDM'): '标本代码',
    ('jybgb', 'BBMC'): '标本名称',
    ('jybgb', 'JYBBH'): '检验标本号',
    ('jybgb', 'BBZT'): '标本状态',
    ('jybgb', 'BBCJBW'): '标本采集部位',
    ('jybgb', 'JSBBSJ'): '接收标本日期',
    ('jybgb', 'JYXMMC'): '检验项目名称',
    ('jybgb', 'JYXMDM'): '检验项目代码',
    ('jybgb', 'JYSQJGMC'): '检验申请机构名称',
    ('jybgb', 'JYJGMC'): '检验机构名称',
    ('jybgb', 'JSBBRQSJ'): '接收标本日期时间',
    ('jybgb', 'JYJSQM'): '检验技师姓名',
    ('jybgb', 'JYJSGH'): '检验技师工号',
    ('jyjgzbb', 'JYZBLSH'): '检验指标流水号',
    ('jyjgzbb', 'YLJGDM'): '医疗机构组织机构代码',
    ('jyjgzbb', 'BGDH'): '检验报告单号',
    ('jyjgzbb', 'BGRQ'): '报告日期',
    ('jyjgzbb', 'JYRQ'): '检验日期',
    ('jyjgzbb', 'JCRGH'): '检测人工号',
    ('jyjgzbb', 'JCRXM'): '检测人姓名',
    ('jyjgzbb', 'SHRGH'): '审核人工号',
    ('jyjgzbb', 'SHRXM'): '审核人姓名',
    ('jyjgzbb', 'JCXMMC'): '检测项目名称',
    ('jyjgzbb', 'JCZBDM'): '检测指标代码',
    ('jyjgzbb', 'JCFF'): '检测方法',
    ('jyjgzbb', 'JCZBMC'): '检测指标名称',
    ('jyjgzbb', 'JCZBJGDX'): '检测指标结果定性',
    ('jyjgzbb', 'JCZBJGDL'): '检测指标结果定量',
    ('jyjgzbb', 'JCZBJGDW'): '检测指标结果定量单位',
    ('jyjgzbb', 'SBBM'): '设备编码',
    ('jyjgzbb', 'YQBH'): '仪器编号',
    ('jyjgzbb', 'YQMC'): '仪器名称',
    ('jyjgzbb', 'CKZFWDX'): '参考值范围(定性)',
    ('jyjgzbb', 'CKZFWXX'): '参考值范围下限',
    ('jyjgzbb', 'CKZFWSX'): '参考值范围上限',
    ('jyjgzbb', 'JLDW'): '计量单位'
}

TYPE_MAPPING = {
    'date': 'time',
    'datetime': 'time',
    'decimal': 'number',
    'int': 'number',
    'text': 'text',
    'varchar': 'text'
}

PRIMARY_KEYS = {
    'yibao': [
        ('t_kc21', 'MED_CLINIC_ID'),
        ('t_kc22', 'MED_EXP_DET_ID'),
        ('t_kc24', 'MED_SAFE_PAY_ID')
    ],
    'yiliao': [
        ('person_info', 'RYBH'),
        ('hz_info', 'KH'),
        ('hz_info', 'KLX'),
        ('hz_info', 'YLJGDM'),
        ('mzjzjlb', 'YLJGDM'),
        ('mzjzjlb', 'JZLSH'),
        ('zyjzjlb', 'YLJGDM'),
        ('zyjzjlb', 'JZLSH'),
        ('jybgb', 'YLJGDM'),
        ('jybgb', 'BGDH'),
        ('jyjgzbb', 'JYZBLSH'),
        ('jyjgzbb', 'YLJGDM')
    ]
}

FOREIGN_KEYS = {
    'yibao': [
        (('t_kc22', 'MED_CLINIC_ID'), ('t_kc21', 'MED_CLINIC_ID')),
        (('t_kc24', 'MED_CLINIC_ID'), ('t_kc21', 'MED_CLINIC_ID'))
    ],
    'yiliao': [
        (('hz_info', 'RYBH'), ('person_info', 'RYBH')),
        (('mzjzjlb', 'YLJGDM'), ('hz_info', 'YLJGDM')),
        (('mzjzjlb', 'KH'), ('hz_info', 'KH')),
        (('mzjzjlb', 'KLX'), ('hz_info', 'KLX')),
        (('zyjzjlb', 'YLJGDM'), ('hz_info', 'YLJGDM')),
        (('zyjzjlb', 'KH'), ('hz_info', 'KH')),
        (('zyjzjlb', 'KLX'), ('hz_info', 'KLX')),
        (('jybgb', 'YLJGDM'), ('mzjzjlb', 'YLJGDM')),
        (('jybgb', 'YLJGDM'), ('zyjzjlb', 'YLJGDM')),
        (('jybgb', 'JZLSH'), ('mzjzjlb', 'JZLSH')),
        (('jybgb', 'JZLSH'), ('zyjzjlb', 'JZLSH')),
        (('jyjgzbb', 'YLJGDM'), ('jybgb', 'YLJGDM')),
        (('jyjgzbb', 'BGDH'), ('jybgb', 'BGDH'))
    ]
}

SQL_KEYWORDS = [
    'SELECT', 'FROM', 'WHERE', 'BY', 'GROUP', 'HAVING', 'ORDER', 'INTERSECT', 'UNION', 'EXCEPT',
    'AVG', 'COUNT', 'MAX', 'MIN', 'SUM', 'DISTINCT',
    'JOIN', 'ON', 'AS',
    'NOT', 'AND', 'OR', 'BETWEEN', 'IN', 'LIKE',
    'ASC', 'DESC', 'LIMIT'
]


def random_split_array(array, ratios=[0.8, 0.1, 0.1]):
    random.shuffle(array)
    result = []
    used_len = 0
    for i, ratio in enumerate(ratios):
        cur_len = int(len(array) * ratio)
        if i == 0:
            result.append(array[:cur_len])
        elif i < len(ratios) - 1:
            result.append(array[used_len:used_len + cur_len])
        else:
            result.append(array[used_len:])
        used_len += cur_len
    return result


def preprocess_sql(sql):
    tokens = sql.replace(',', ' , ').replace('(', ' ( ').replace(')', ' ) ').split()
    while '' in tokens:
        tokens.remove('')
    for i in range(len(tokens)):
        if tokens[i] in SQL_KEYWORDS:
            tokens[i] = tokens[i].lower()
    return ' '.join(tokens)


def parse_sql(schema, sql):
    pass


def generate_db_content():
    db_content = []
    _, common_cursor = connect_database('information_schema')
    for schema in ['yibao', 'yiliao']:
        tables = {}
        _, cursor = connect_database(schema)
        common_cursor.execute('SELECT table_name FROM tables WHERE table_schema = %s', [schema])
        table_names = [item[0] for item in common_cursor.fetchall()]
        for table_name in table_names:
            cursor.execute(f'SELECT * FROM {table_name}')
            common_cursor.execute('SELECT column_name, data_type FROM columns WHERE table_schema = %s AND table_name = %s', [schema, table_name])
            columns = common_cursor.fetchall()
            tables[TABLE_MAPPING[table_name]] = {
                'cell': [[str(item) for item in record] for record in cursor.fetchall()],
                'header': [column[0] for column in columns],
                'table_name': table_name,
                'type': [TYPE_MAPPING[column[1]] for column in columns]
            }
        db_content.append({
            'db_id': SCHEMA_MAPPING[schema],
            'tables': tables
        })
    with open('ylsql/db_content.json', 'w', encoding='utf-8') as file:
        json.dump(db_content, file, ensure_ascii=False, indent=4)


def generate_tables():
    tables = []
    schemata = {}
    _, common_cursor = connect_database('information_schema')
    for schema in ['yibao', 'yiliao']:
        common_cursor.execute('SELECT table_name FROM tables WHERE table_schema = %s', [schema])
        table_names = [item[0] for item in common_cursor.fetchall()]
        column_names = []
        column_types = ['text']
        for i, table_name in enumerate(table_names):
            common_cursor.execute('SELECT column_name, data_type FROM columns WHERE table_schema = %s AND table_name = %s', [schema, table_name])
            columns = common_cursor.fetchall()
            column_names.extend([[i, column[0]] for column in columns])
            column_types.extend([TYPE_MAPPING[column[1]] for column in columns])
        column_ids = {}
        for i, column_name in enumerate(column_names):
            column_ids[(table_names[column_name[0]], column_name[1])] = i + 1
        tables.append({
            'db_id': SCHEMA_MAPPING[schema],
            'table_names': [TABLE_MAPPING[table_name] for table_name in table_names],
            'column_names': [[-1, '*']] + [[column_name[0], COLUMN_MAPPING[(table_names[column_name[0]], column_name[1])]] for column_name in column_names],
            'table_names_original': table_names,
            'column_names_original': [[-1, '*']] + column_names,
            'column_types': column_types,
            'foreign_keys': [[column_ids[foreign_key[0]], column_ids[foreign_key[1]]] for foreign_key in FOREIGN_KEYS[schema]],
            'primary_keys': [column_ids[primary_key] for primary_key in PRIMARY_KEYS[schema]]
        })
        schemata[schema] = column_ids
    with open('ylsql/tables.json', 'w', encoding='utf-8') as file:
        json.dump(tables, file, ensure_ascii=False, indent=4)
    return schemata


def generate_train_or_dev(train_or_dev_set, set_name, schemata):
    pass


def generate_train_or_dev_gold(train_or_dev_set, set_name):
    with open(f'ylsql/{set_name}_gold.sql', 'w', encoding='utf-8') as file:
        for i, example in enumerate(train_or_dev_set):
            file.write(f"qid{str(i + 1).zfill(6)}\t{preprocess_sql(example['sql'])}\t{example['schema']}\n")


def generate_test(test_set):
    result = []
    for i, example in enumerate(test_set):
        result.append({
            'query': '',
            'db_id': example['schema'],
            'question': example['question'],
            'sql': '',
            'question_id': f'qid{str(i + 1).zfill(6)}'
        })
    with open('ylsql/test.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--split', type=str, choices=['example', 'template'], required=True)
args = arg_parser.parse_args()
with open('dataset/dataset.json', 'r', encoding='utf-8') as file:
    dataset = json.load(file)
if args.split == 'example':
    train, dev, test = random_split_array(dataset)
elif args.split == 'template':
    templates = []
    for example in dataset:
        if len(templates) == 0 or example['template'] > templates[-1]:
            templates.append(example['template'])
    train_templates, dev_templates, test_templates = random_split_array(templates)
    train = [example for example in dataset if example['template'] in train_templates]
    dev = [example for example in dataset if example['template'] in dev_templates]
    test = [example for example in dataset if example['template'] in test_templates]
else:
    raise ValueError(f'unknown split method {args.split}')
generate_db_content()
schemata = generate_tables()
generate_train_or_dev(train, 'train', schemata)
generate_train_or_dev(dev, 'dev', schemata)
generate_train_or_dev_gold(train, 'train')
generate_train_or_dev_gold(dev, 'dev')
generate_test(test)
