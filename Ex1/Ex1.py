'''
#代表全国图鉴编号，不同行存在相同数字则表示为该妖怪的不同状态
妖怪具有单属性和和双属性两种，对于单属性的妖怪，Type2为缺失值
Total、HP、Attack、Defense、Sp.Def、Speed分别代表
种族值、体力、物攻、防御、特攻、特防、速度，其中种族值为六项之和
questions:
1. 对 HP, Attack, Defense, Sp. Atk, Sp. Def, Speed 进行加总，验证是否为 Total 值。
2. 对于 #重复的妖怪只保留第一条记录，解决以下问题：
(a) 求第一属性的种类数量和前三多数量对应的种类
(b) 求第一属性和第二属性的组合种类
(c) 求尚未出现过的属性组合
3. 按照下述要求，构造Series ：
(a) 取出物攻，超过120 的替换为high ，不足50的替换为low，否则设为mid
(b) 取出第一属性，分别用replace 和 apply 替换所有字母为大写
(c) 求每个妖怪六项能力的离差，即所有能力中偏离中位数最大的值，添加到df并从大到小排序
'''


import pandas as pd
import numpy as np

#读取数据
df = pd.read_csv('data/pokemon.csv')

#验证Total是否为6项之和
stats = ['HP','Attack','Defense','Sp. Atk','Sp. Def','Speed']
df['Total_calc'] = df[stats].sum(axis=1)
is_total_valid = (df['Total'] == df['Total_calc']).all()
print( f"Total 是否等于后6项之和：{is_total_valid}")

#重复的记录只保留第一条
df_unique = df.drop_duplicates(subset='#',keep='first').copy()
#第一属性的种类数量，以及前三多数量对应的种类
type1_counts = df_unique['Type 1'].value_counts()
print(f"\n2(a) 第一属性种类数量：{type1_counts.shape[0]}")
print("前三多数量对应的种类：")
print(type1_counts.head(3))

#第一属性和第二属性的组合种类
#将缺失的Type2 填充为'None'，方便组合
df_unique['Type 2'] = df_unique['Type 2'].fillna('None')
combos = df_unique.groupby(['Type 1','Type 2']).size().reset_index(name = 'count')
print(f"\n2(b) 第一属性和第二属性的组合种类数量：{combos.shape[0]}")
print(combos.head())

#尚未出现过的属性组合 获取所有出现过的属性（排除'None'）
all_types = pd.concat([df_unique['Type 1'],df_unique['Type 2']]).unique()
all_types = [t for t in all_types if t != 'None']

#生成所有可能的组合（包含单属性，即 Type 2 为 'None')
all_combos = set()
for t1 in all_types:
    all_combos.add((t1,'None'))   #单属性
    for t2 in all_types:
        if t1 != t2:
            all_combos.add((t1, t2))  #双属性，有顺序
            all_combos.add((t2, t1))  #反向组合也视为不同
# 已出现的组合
existing_combos = set(zip(df_unique['Type 1'],df_unique['Type 2']))
missing_combos =  all_combos - existing_combos
print(f"\n2(c) 尚未出现过的属性组合数量：{len(missing_combos)}")
print("部分未出现组合示例：")
print(list(missing_combos)[:10])

#构造 Series 物攻分类：>120为high，<50 为low，其余为mid
def attack_level(x):
    if x > 120:
        return 'high'
    elif x < 50:
        return 'low'
    else:
        return 'mid'
attack_series = df_unique['Attack'].apply(attack_level)
print("\n3(a) 物攻分类 Series 前 5 个:")
print(attack_series.head())

# 第一属性大写：分别用 replace 和 apply
# 方法一：replace
type1_upper_replace = df_unique['Type 1'].replace({t: t.upper() for t in df_unique['Type 1'].unique()})
# 方法二：apply
type1_upper_apply = df_unique['Type 1'].apply(lambda x: x.upper())
print("\n3(b) 用 replace 替换大写前 5 个:")
print(type1_upper_replace.head())
print("用 apply 替换大写前 5 个:")
print(type1_upper_apply.head())
# (c) 求每个妖怪六项能力的离差，即所有能力中偏离中位数最大的值
def max_deviation(row):
    values = row[stats].values
    median = np.median(values)
    return np.max(np.abs(values - median))

df_unique['Deviation'] = df_unique.apply(max_deviation, axis=1)
df_unique_sorted = df_unique.sort_values('Deviation', ascending=False)

print("\n3(c) 按离差从大到小排序（前 10 行）:")
print(df_unique_sorted[['Name', 'Deviation']].head(10))
