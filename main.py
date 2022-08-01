from generate_dataset import generate_dataset
from generate_yibao import generate_yibao
from generate_yiliao import generate_yiliao

value_sets = generate_dataset()
generate_yibao(value_sets)
generate_yiliao(value_sets)
