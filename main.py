from generate_dataset.generate_dataset import generate_dataset
from generate_dataset.generate_excel import generate_excel
from generate_dataset.generate_yibao import generate_yibao
from generate_dataset.generate_yiliao import generate_yiliao

dataset, value_sets = generate_dataset()
generate_excel(dataset)
generate_yibao(value_sets)
generate_yiliao(value_sets)
