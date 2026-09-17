import numpy as np
import pandas as pd
#pandas 读取文件
df_csv = pd.read_csv('ch2/my_csv.csv')
df_txt = pd.read_table('ch2/my_table.txt')
df_excel = pd.read_excel('ch2/my_excel.xlsx')
# header=None表示第一行不作为列名
pd.read_table('ch2/my_table.txt',header=None)
# index_col表示把某一列或几列作为索引
pd.read_csv('ch2/my_csv.csv',index_col=['col1','col2'])
# usecols 表示读取列的集合，默认读取所有的列
# parse_dates 表示需要转化为时间的列
pd.read_csv('ch2/my_csv.csv',parse_dates=['col5'])
# nrows 表示读取的数据行数
pd.read_excel('ch2/my_excel.xlsx',nrows=2)
# sep分割参数
pd.read_table('ch2/my_table_special_sep.txt', sep=' \|\|\|\| ',engine='python')

# 数据写入 当索引没有特殊意义的时候，把index设置为False可以把索引在保存的时候去除
df_csv.to_csv('chw/my_csv_saved.csv', index=False)
df_excel.to_excel('data/my_excel_saved.xlsx',index=False)
#pandas中没有定义to_table函数，但是to_csv可以保存为txt文件，并且允许自定义分隔符，常用制表符\t分割
df_txt.to_csv('data/my_txt_saved.txt',sep='\t', index=False)
# 表格转换：to_markdown、to_;atex（需要tabulate包）

#-------------------------------------------
# 基本数据结构
#pandas具有两种基本的数据存储结构：Series\DataFrame
#Series一般由四个部分组成，分别为data、index、dtype、name
#head\tail 函数分别表示返回表或者序列的前n行和后n行
#info/describe分别返回表的信息概况和表中数值列对应的主要统计量
#quantile返回分位数
#count返回非缺失值个数
#idxmax返回最大值对应的索引
#unique 和 nunique分别得到唯一值组成的列表和唯一值的个数
#value_counts可以得到唯一值和其对应出现的频数
#drop_duplicates 观察多个列组合的唯一值
#数值替换包含round取整、abs取绝对值、clip截断
#在clip中，超过边界的只能截断为边界值，如果要把超出边界的替换为自定义的值，应当如何做？
s = pd.Series([-5, 0, 5, 10, 15])
lower,upper = 0,10
low_replace, high_replace = -999, 999
result = s.mask(s < lower, low_replace).mask(s > upper, high_replace)
#-------------------------------------------
#窗口对象，滑动窗口rolling、扩张窗口expanding、指数加权窗口ewn

