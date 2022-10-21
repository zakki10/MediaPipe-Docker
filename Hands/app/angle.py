import numpy as np
import math
'''
a = np.array([-0.0069, -0.0022, -0.0080])
b = np.array([-0.0176, 0.0020, -0.0114])
c = np.array([-0.0287, 0.0181, 0.0053])
'''

a = np.array([-0.0069, -0.0022])
b = np.array([-0.0176, 0.0020])
c = np.array([-0.0287, 0.0181])

# ベクトルを定義
vec_a = a - b
vec_c = c - b

# コサインの計算
length_vec_a = np.linalg.norm(vec_a)
length_vec_c = np.linalg.norm(vec_c)
inner_product = np.inner(vec_a, vec_c)
cos = inner_product / (length_vec_a * length_vec_c)

# 角度（ラジアン）の計算
rad = np.arccos(cos)

# 弧度法から度数法（rad ➔ 度）への変換
degree = np.rad2deg(rad)

print(degree)