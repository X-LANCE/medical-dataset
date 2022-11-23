import jieba
import json
import os
import pandas as pd
import pickle
import random
from xeger import Xeger
from util.constant import DEPT_NAMES, DISEASE_NAMES, MEDICINE_NAMES, TESTING_INDEX_NAMES, BODY_PART_NAMES
from util.util import generate_date, generate_two_dates, generate_last_name, generate_name


class PlaceHolder:
    def __init__(self, string, types, func=None, pattern=None, values=None):
        assert string.count('$') == len(types)
        self.string = string
        self.types = types
        self.func = func
        self.pattern = pattern
        self.values = values

    def generate(self):
        string = ''
        if self.func is None:
            values = []
            for char in self.string:
                if char == '$':
                    if self.pattern is None:
                        if isinstance(self.values[0], list):
                            tmp_values = random.choice(self.values)
                            values.append(tmp_values[0])
                            string += random.choice(tmp_values)
                        else:
                            values.append(random.choice(self.values))
                            string += values[-1]
                    else:
                        values.append(Xeger().xeger(self.pattern))
                        string += values[-1]
                else:
                    string += char
        else:
            values = self.func()
            idx = 0
            for char in self.string:
                if char == '$':
                    string += values[idx]
                    idx += 1
                else:
                    string += char
        return string, values


def get_partial_values(all_values):
    partial_values = set()
    for values in all_values:
        if not isinstance(values, list):
            values = [values]
        for value in values:
            words = list(jieba.cut(value))
            for word in words:
                partial_values.add(word)
    return list(partial_values)


def fix_many_foreign_keys(dataset):
    fixed_foreign_keys = [
        ('mzjzjlb.YLJGDM = jybgb.YLJGDM', 'mzjzjlb.YLJGDM = jybgb.YLJGDM_MZJZJLB'),
        ('zyjzjlb.YLJGDM = jybgb.YLJGDM', 'zyjzjlb.YLJGDM = jybgb.YLJGDM_ZYJZJLB'),
        ('mzjzjlb.JZLSH = jybgb.JZLSH', 'mzjzjlb.JZLSH = jybgb.JZLSH_MZJZJLB'),
        ('zyjzjlb.JZLSH = jybgb.JZLSH', 'zyjzjlb.JZLSH = jybgb.JZLSH_ZYJZJLB')
    ]
    for i in range(len(dataset)):
        for fixed_foreign_key in fixed_foreign_keys:
            dataset[i]['sql'] = dataset[i]['sql'].replace(fixed_foreign_key[0], fixed_foreign_key[1])
    return dataset


def generate_dataset():
    place_holders = {
        '整数': PlaceHolder('$', ['number'], func=lambda : [str(random.randint(1, 30))]),
        '小实数': PlaceHolder('$', ['number'], func=lambda : [str(round(random.uniform(0, 1), 2))]),
        '大实数': PlaceHolder('$', ['number'], func=lambda : [str(round(random.uniform(0, 10000), 2))]),
        '时间': PlaceHolder('$', ['text'], func=lambda : [generate_date()]),
        '时间段': PlaceHolder('$到$', ['text', 'text'], func=generate_two_dates),
        '医疗就诊ID': PlaceHolder('$', ['text'], pattern=r'\d{11}'),
        '人员ID': PlaceHolder('$', ['text'], pattern=r'\d{8}'),
        '人员姓名': PlaceHolder('$', ['text'], func=lambda : [generate_name()]),
        '人员姓': PlaceHolder('$', ['right_fuzzy'], func=lambda : [generate_last_name()]),
        '医疗机构代码': PlaceHolder('$', ['text'], pattern=r'\d{7}'),
        '疾病编码': PlaceHolder('$', ['text'], pattern=r'[A-Z]\d{2}\.(\d|X)\d{2}'),
        '疾病名称': PlaceHolder('$', ['text'], values=DISEASE_NAMES),
        '部分疾病名称': PlaceHolder('$', ['left_right_fuzzy'], values=get_partial_values(DISEASE_NAMES)),
        '科室编码': PlaceHolder('$', ['text'], pattern=r'\d{3,5}'),
        '科室名称': PlaceHolder('$', ['text'], values=DEPT_NAMES),
        '部分科室名称': PlaceHolder('$', ['left_right_fuzzy'], values=get_partial_values(DEPT_NAMES)),
        '人员医疗费用明细ID': PlaceHolder('$', ['text'], pattern=r'\d{11}'),
        '社保三大目录统一编码': PlaceHolder('$', ['text'], pattern=r'(\d{4}|\d{6}|\d{9})(-(\d|[a-z]))?'),
        '社保三大目录名称': PlaceHolder('$', ['text'], values=MEDICINE_NAMES),
        '部分社保三大目录名称': PlaceHolder('$', ['left_right_fuzzy'], values=get_partial_values(MEDICINE_NAMES)),
        '门诊就诊流水号': PlaceHolder('$', ['text'], pattern=r'\d{11}'),
        '住院就诊流水号': PlaceHolder('$', ['text'], pattern=r'\d{11}'),
        '门诊就诊流水号或住院就诊流水号': PlaceHolder('$', ['text'], pattern=r'\d{11}'),
        '医生工号': PlaceHolder('$', ['text'], pattern=r'\d{8}'),
        '检验报告单号': PlaceHolder('$', ['text'], pattern=r'\d{11}'),
        '检验指标流水号': PlaceHolder('$', ['text'], pattern=r'\d{11}'),
        '检测人工号': PlaceHolder('$', ['text'], pattern=r'\d{8}'),
        '检测人姓名': PlaceHolder('$', ['text'], func=lambda : [generate_name()]),
        '检测指标代码': PlaceHolder('$', ['text'], pattern=r'\d{6}'),
        '检测指标名称': PlaceHolder('$', ['text'], values=TESTING_INDEX_NAMES),
        '部位': PlaceHolder('$', ['text'], values=BODY_PART_NAMES)
    }
    if os.path.exists('resource/dataset.json') and os.path.exists('resource/value_sets.bin'):
        with open('resource/dataset.json', 'r', encoding='utf-8') as file:
            dataset = json.load(file)
        with open('resource/value_sets.bin', 'rb') as file:
            value_sets = pickle.load(file)
        example_id = len(dataset)
    else:
        dataset = []
        value_sets = {}
        for key in place_holders:
            value_sets[key] = set()
        example_id = 0
    data = pd.read_excel('resource/templates.xlsx', skiprows=10)
    for i in range(len(data)):
        if (len(dataset) > 0 and i <= dataset[-1]['template']) or data['难度'][i] == '不可回答':
            continue
        question_template = data['查询模板'][i]
        sql_template = data['SQL模板'][i]
        for _ in range(10):
            all_values = []
            all_types = []
            question = ''
            end = -1
            while 1:
                start = question_template[end + 1:].find('（') + end + 1
                if start <= end:
                    question += question_template[end + 1:]
                    break
                question += question_template[end + 1:start]
                end = question_template[start:].find('）') + start
                place_holder = question_template[start + 1:end]
                string, values = place_holders[place_holder].generate()
                question += string
                all_values.extend(values)
                all_types.extend(place_holders[place_holder].types)
                value_sets[place_holder].update(values)
            sql = ''
            end = -1
            while 1:
                start = sql_template[end + 1:].find('$') + end + 1
                if start <= end:
                    sql += sql_template[end + 1:]
                    break
                sql += sql_template[end + 1:start]
                end = start + 1
                while end + 1 < len(sql_template) and sql_template[end + 1] >= '0' and sql_template[end + 1] <= '9':
                    end += 1
                idx = int(sql_template[start + 1:end + 1]) - 1
                if all_types[idx] == 'number':
                    sql += all_values[idx]
                elif all_types[idx] == 'text':
                    sql += f"'{all_values[idx]}'"
                elif 'fuzzy' in all_types[idx]:
                    sql += "'"
                    if 'left' in all_types[idx]:
                        sql += '%'
                    sql += all_values[idx]
                    if 'right' in all_types[idx]:
                        sql += '%'
                    sql += "'"
                else:
                    raise ValueError
            dataset.append({
                'id': example_id,
                'template': i,
                'question': question,
                'sql': sql,
                'schema': data['数据库'][i],
                'level': data['难度'][i]
            })
            example_id += 1
    dataset = fix_many_foreign_keys(dataset)
    with open('resource/dataset.json', 'w', encoding='utf-8') as file:
        json.dump(dataset, file, ensure_ascii=False, indent=4)
    with open('resource/value_sets.bin', 'wb') as file:
        pickle.dump(value_sets, file)
    for key in value_sets:
        value_sets[key] = list(value_sets[key])
    return dataset, value_sets
