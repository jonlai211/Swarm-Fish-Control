# -*- coding: utf-8 -*-
# @Author  : JonathanLai
# @Time    : 7/19/23 3:05 PM
# @File    : onnx_check.py

import onnx

onnx_model = onnx.load("best.onnx")

onnx.checker.check_model(onnx_model)

print('no problem')
print(onnx.helper.printable_graph(onnx_model.graph))

# .onnx file can be opened in https://netron.app/
