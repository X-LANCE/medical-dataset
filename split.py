import copy
import json
import random
from util.util import random_split_array


def generate_subset(subset, split_method, set_name):
    assert split_method in ['example', 'schema', 'template']
    assert set_name in ['train', 'dev', 'test']
    for i, example in enumerate(subset):
        example['question_id'] = f'qid{str(i + 1).zfill(5)}'
        example.pop('template_id')
    with open(f'data/mdsql/{split_method}/{set_name}.json', 'w', encoding='utf-8') as file:
        json.dump(subset, file, ensure_ascii=False, indent=4)


def split_example(dataset):
    dataset = [example for example in dataset if example['db_id'] in ['医保表', '医疗表']]
    train, dev, test = random_split_array(dataset)
    generate_subset(train, 'example', 'train')
    generate_subset(dev, 'example', 'dev')
    generate_subset(test, 'example', 'test')


def split_template(dataset):
    dataset = [example for example in dataset if example['db_id'] in ['医保表', '医疗表']]
    templates = set()
    for example in dataset:
        templates.add(example['template_id'])
    train_templates, dev_templates, test_templates = random_split_array(sorted(list(templates)))
    train = [example for example in dataset if example['template_id'] in train_templates]
    dev = [example for example in dataset if example['template_id'] in dev_templates]
    test = [example for example in dataset if example['template_id'] in test_templates]
    random.shuffle(train)
    random.shuffle(dev)
    random.shuffle(test)
    generate_subset(train, 'template', 'train')
    generate_subset(dev, 'template', 'dev')
    generate_subset(test, 'template', 'test')


def split_schema(dataset):
    schemata = set()
    for example in dataset:
        schemata.add(example['db_id'])
    while 1:
        train_schemata, dev_schemata, test_schemata = random_split_array(sorted(list(schemata)))
        if '医保表' in train_schemata and '医疗表' in train_schemata:
            break
    train = [example for example in dataset if example['db_id'] in train_schemata]
    dev = [example for example in dataset if example['db_id'] in dev_schemata]
    test = [example for example in dataset if example['db_id'] in test_schemata]
    random.shuffle(train)
    random.shuffle(dev)
    random.shuffle(test)
    generate_subset(train, 'schema', 'train')
    generate_subset(dev, 'schema', 'dev')
    generate_subset(test, 'schema', 'test')


random.seed(42)
with open('data/mdsql/all.json', 'r', encoding='utf-8') as file:
    dataset_origin = json.load(file)
dataset = copy.deepcopy(dataset_origin)
split_example(dataset)
dataset = copy.deepcopy(dataset_origin)
split_template(dataset)
dataset = copy.deepcopy(dataset_origin)
split_schema(dataset)
