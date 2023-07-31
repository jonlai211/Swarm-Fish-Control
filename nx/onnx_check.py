# -*- coding: utf-8 -*-
# @Author  : JonathanLai
# @Time    : 7/19/23 3:05 PM
# @File    : onnx_check.py

import nx

onnx_model = nx.load("best.nx")

nx.checker.check_model(onnx_model)

print('no problem')
print(nx.helper.printable_graph(onnx_model.graph))

# .nx file can be opened in https://netron.app/
