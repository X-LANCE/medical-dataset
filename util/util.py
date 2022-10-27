import pymysql
import random
from datetime import date, datetime
from util.constant import LAST_NAMES, MALE_FIRST_NAMES, FEMALE_FIRST_NAMES, REGIONS, SQL_AGGS


def generate_date():
    year = random.randint(2000, 2021)
    month = random.randint(1, 12)
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    elif month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    elif (year % 4 == 0 and year % 100 > 0) or year % 400 == 0:
        day = random.randint(1, 29)
    else:
        day = random.randint(1, 28)
    return f'{year}-{str(month).zfill(2)}-{str(day).zfill(2)}'


def generate_two_dates():
    while 1:
        first_date = generate_date()
        second_date = generate_date()
        if first_date < second_date:
            break
    return [first_date, second_date]


def generate_last_name():
    return random.choice(LAST_NAMES)


def generate_name():
    sex = random.randint(0, 1)
    return generate_last_name() + (random.choice(MALE_FIRST_NAMES) if sex == 0 else random.choice(FEMALE_FIRST_NAMES))


def generate_datetime():
    return f'{generate_date()} {str(random.randint(0, 23)).zfill(2)}:{str(random.randint(0, 59)).zfill(2)}:{str(random.randint(0, 59)).zfill(2)}'


def generate_date_of_birth(latest_date):
    year = int(latest_date[:4]) - random.randint(1, 100)
    month = random.randint(1, 12)
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    elif month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    elif (year % 4 == 0 and year % 100 > 0) or year % 400 == 0:
        day = random.randint(1, 29)
    else:
        day = random.randint(1, 28)
    return f'{year}-{str(month).zfill(2)}-{str(day).zfill(2)}'


def generate_region():
    return random.choice(REGIONS)


def generate_medical_index(medical_project):
    if medical_project == '肝功能':
        return random.choice([
            ('总胆红素三代', '重氮法', 'umol/L', 0, 21),
            ('直接胆红素二代', '重氮法', 'umol/L', 0, 5),
            ('总蛋白', '双缩脲法', 'g/L', 66, 87),
            ('白蛋白', '溴甲酚绿法', 'g/L', 35, 52),
            ('脂肪酶', '比色法', 'U/L', 13, 60),
            ('前白蛋白', '免疫比浊法', 'mg/dL', 20, 40)
        ])
    if medical_project == '肾功能':
        return random.choice([
            ('尿素', '酶动力学法', 'mmol/L', 2.76, 8.07),
            ('胱抑素C2代', '免疫透射比浊法', 'mg/L', 0.61, 0.95),
            ('同型半胱氨酸', '酶法', 'umol/L', 0, 12)
        ])
    if medical_project == '糖代谢':
        return '果糖胺', '比色法', 'umol/L', 205, 285
    if medical_project == '血脂':
        return random.choice([
            ('甘油三酯', '酶比色法', 'mmol/L', 0, 1.7),
            ('甘油三酯', '去甘油法', 'mmol/L', 0, 1.7),
            ('胆固醇', 'ID/MS', 'mmol/L', 0, 5.17),
            ('胆固醇', 'Abell/Kendall', 'mmol/L', 0, 5.17),
            ('低密度脂蛋白胆固醇', '均相酶比色法', 'mmol/L', 0, 2.59),
            ('脂蛋白(a)二代', '免疫透射比浊法', 'nmol/L', 0, 75)
        ])
    if medical_project == '心肌酶':
        return random.choice([
            ('肌酸激酶同工酶', '酶比色法', 'U/L', 0, 25),
            ('α-羟丁酸脱氢酶', '酶比色法', 'U/L', 72, 182)
        ])
    if medical_project == '离子类':
        return '二氧化碳', '比色法', 'mmol/L', 22, 29
    if medical_project == '风湿三项':
        return random.choice([
            ('类风湿因子', '免疫比浊法', 'IU/mL', 0, 14),
            ('C反应蛋白', '免疫透射比浊法', 'mg/L', 0, 5),
            ('C反应蛋白', '胶乳免疫透射比浊法', 'mg/L', 0, 5)
        ])
    if medical_project == '特定蛋白':
        return random.choice([
            ('补体C3', '免疫比浊法', 'g/L', 0.9, 1.8),
            ('补体C4', '免疫比浊法', 'g/L', 0.1, 0.4),
            ('免疫球蛋白A(标准)', '免疫比浊法', 'g/L', 0.7, 4),
            ('免疫球蛋白A(敏感)', '免疫比浊法', 'g/L', 0.7, 4),
            ('免疫球蛋白M(标准)', '免疫比浊法', 'g/L', 0.4, 2.3),
            ('免疫球蛋白M(敏感)', '免疫比浊法', 'g/L', 0.4, 2.3),
            ('a1酸性糖蛋白', '免疫比浊法', 'g/L', 0.5, 1.2),
            ('a1抗胰蛋白酶', '免疫比浊法', 'g/L', 0.9, 2),
            ('抗凝血酶III', '免疫比浊法', '%', 80, 120),
            ('D2聚体(柠檬酸盐)', '免疫比浊法', 'ug FEU/mL', 0, 0.5),
            ('D2聚体(肝素/EDTA)', '免疫比浊法', 'ug FEU/mL', 0, 0.5),
            ('触珠蛋白', '免疫比浊法', 'g/L', 0.3, 2),
            ('B2微球蛋白', '免疫比浊法', 'mg/L', 0.8, 2.2)
        ])
    if medical_project == '铁代谢':
        return random.choice([
            ('血清铁', '比色法', 'umol/L', 5.83, 34.5),
            ('转铁蛋白', '免疫比浊法', 'g/L', 2, 3.6)
        ])
    if medical_project == '尿蛋白':
        return '胸腹水白蛋白(白蛋白)', '免疫比浊法', 'g/L', 35, 52
    if medical_project == '治疗药物检测':
        return random.choice([
            ('苯巴比妥', '溶液动态微粒子', 'ug/mL', 10, 30),
            ('苯妥因', '溶液动态微粒子', 'ug/mL', 10, 20),
            ('茶碱', '溶液动态微粒子', 'ug/mL', 10, 20),
            ('丙戊酸', '酶免分析放大技术', 'ug/mL', 50, 100)
        ])
    if medical_project == '肿瘤标志物':
        return random.choice([
            ('甲胎蛋白', '夹心法', 'ng/mL', 0, 7),
            ('糖类抗原125', '夹心法', 'U/mL', 0, 35),
            ('糖类抗原724', '夹心法', 'U/mL', 0, 6.9),
            ('游离前列腺特异性抗原', '夹心法', 'ng/mL', 0, 0.93),
            ('胃泌素释放肽前体', '夹心法', 'pg/mL', 28.3, 74.4),
            ('神经元特异性烯醇化酶', '夹心法', 'ng/mL', 0, 16.3),
            ('细胞角蛋白19片段', '夹心法', 'ng/mL', 0, 3.3),
            ('罗马指数(绝经前)', '计算', '%', 0, 11.4),
            ('罗马指数(绝经后)', '计算', '%', 0, 29.9),
            ('S100', '夹心法', 'ug/L', 0, 0.105)
        ])
    if medical_project == '甲状腺':
        return random.choice([
            ('三碘甲状腺原氨酸', '竞争法', 'nmol/L', 1.3, 3.1),
            ('甲状腺素', '竞争法', 'nmol/L', 66, 181),
            ('游离三碘甲状腺原氨酸', '竞争法', 'pmol/L', 3.1, 6.8),
            ('游离甲状腺素', '竞争法', 'pmol/L', 12, 22),
            ('游离甲状腺素(三代)', '竞争法', 'pmol/L', 12, 22),
            ('促甲状腺激素', '夹心法', 'uIU/mL', 0.27, 4.2),
            ('甲状腺过氧化物酶抗体', '竞争法', 'IU/mL', 0, 34),
            ('促甲状腺激素受体抗体', '竞争法', 'IU/L', 0, 1.75),
            ('超敏甲状腺球蛋白', '夹心法', 'ng/mL', 3.5, 77),
            ('甲状腺摄取实验', '改良竞争法', 'TBI', 0.8, 1.3)
        ])
    if medical_project == '激素':
        return '促肾上腺皮质激素', '夹心法', 'ng/L', 7.2, 63.3
    if medical_project == '产筛':
        return random.choice([
            ('妊娠相关性血浆蛋白-A', '双抗体夹心法', 'mIU/L', 0, 7.15),
            ('游离β-绒毛膜促性腺激素', '夹心法', 'IU/L', 0, 0.1)
        ])
    if medical_project == '心肌':
        return random.choice([
            ('氨基末端B型利钠肽', '夹心法', 'pg/mL', 0, 125),
            ('超敏肌钙蛋白T', '夹心法', 'pg/mL', 0, 14),
            ('地高辛', '竞争法', 'nmol/L', 0.77, 1.5),
            ('洋地黄', '竞争法', 'nmol/L', 13, 33)
        ])
    if medical_project == '传染病':
        return '乙肝表面抗原(定量)', '夹心法', 'IU/mL', 0, 0.05
    if medical_project == '骨标志物':
        return random.choice([
            ('甲状旁腺素', '夹心法', 'pg/mL', 15, 65),
            ('全段甲状旁腺激素', '夹心法', 'pg/mL', 14.9, 56.9)
        ])
    if medical_project == '贫血':
        return random.choice([
            ('叶酸', '竞争法', 'ng/mL', 4.6, 34.8),
            ('叶酸', '竞争法', 'nmol/L', 10.4, 78.9)
        ])
    if medical_project == '脓毒血症':
        return random.choice([
            ('白介素-6', '夹心法', 'pg/mL', 0, 7),
            ('降钙素原', '夹心法', 'ng/mL', 0, 0.05)
        ])
    if medical_project == '类风关':
        return '抗环瓜氨酸肽抗体', 'IgG-捕获法', 'U/mL', 0, 17
    raise ValueError


def calculate_code(id_number):
    coefficients = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    code = 0
    for i in range(len(coefficients)):
        code += coefficients[i] * int(id_number[i])
    code = (12 - code % 11) % 11
    return str(code) if code < 10 else 'X'


def str_to_date(string):
    return date(int(string[:4]), int(string[5:7]), int(string[8:]))


def str_to_datetime(string):
    return datetime(int(string[:4]), int(string[5:7]), int(string[8:10]), int(string[11:13]), int(string[14:16]), int(string[17:]))


def str_to_number(string):
    try:
        return int(string)
    except:
        return float(string)


def random_split_number(number, segment):
    points = [0, number]
    for _ in range(segment - 1):
        points.append(round(random.uniform(0, number), 2))
    points.sort()
    result = []
    for i in range(segment):
        result.append(round(points[i + 1] - points[i], 2))
    return result


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


def connect_database(database_name):
    database = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database=database_name)
    cursor = database.cursor()
    return database, cursor


def update_database(database, cursor, table, data):
    sql = f'INSERT INTO {table}('
    for key in vars(data[0]):
        sql += key + ', '
    sql = sql[:-2] + ') VALUES(' + '%s, ' * len(vars(data[0]))
    sql = sql[:-2] + ')'
    for record in data:
        cursor.execute(sql, list(vars(record).values()))
        database.commit()


def skip_nested(tokens, start):
    assert tokens[start - 1] == '('
    count = 1
    end = start
    while count > 0:
        if tokens[end] == '(' or (tokens[end][:-1] in SQL_AGGS and tokens[end][-1] == '('):
            count += 1
        elif tokens[end] == ')':
            count -= 1
        end += 1
    return end
