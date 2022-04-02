import pprint

import numpy as np
import pandas as pd

data = {}
data['userid'] = np.random.randint(0, 3, (21,))
data['itemid'] = np.random.randint(0, 10, (21,))
data['timestamp'] = np.array(['20190101','20190102','20190103','20190104','20190105','20190106','20190107','20190108','20190109',
                       '20190110','20190111','20190112','20190113','20190114','20190115','20190116','20190117','20190118',
                       '20190119','20190120','20190121'])
df = pd.DataFrame(data=data)
df['timestamp'] = pd.to_datetime(df['timestamp'])


data_cate = {}
data_cate['itemid'] = np.array([0,1,2,3,4,5,6,7,8,9,10])
data_cate['categoryid'] = np.array([0,0,0,1,1,1,2,2,2,3,3])
df_cate = pd.DataFrame(data=data_cate)
df = pd.merge(df, df_cate, how='left', on='itemid')
df = df[['userid','itemid','categoryid','timestamp']]
df = df.sort_values(by=['userid','itemid']).reset_index(drop=True)
print('例示用')
print(df)


# 用户ID，按时间顺序排序
df_seq = df.sort_values(by=['userid','timestamp'])
# groupby作为一个列表，以每个用户为基础。
df_seq = df_seq.groupby('userid').agg(list).reset_index(drop=False)

# 值检索
print('每个用户接触过的item-ID（按时间顺序排列）')
pprint.pprint(df_seq['itemid'].values.tolist())
print('每个用户联系过的categoryid（按时间顺序排列）')
pprint.pprint(df_seq['categoryid'].values.tolist())

# groupby来获取每个用户的最新数据。
df_cate = df.loc[df.groupby('userid')['timestamp'].idxmax()]

print(df_cate)
print('每个用户最近接触过的-itemid')
pprint.pprint(df_cate['itemid'].values.tolist())
print('每个用户最近接触过的categoryid')
pprint.pprint(df_cate['categoryid'].values.tolist())

import tensorflow as tf
inputs = []
inputs.append(tf.keras.preprocessing.sequence.pad_sequences(
    df_seq['itemid'].values.tolist(), padding='post', truncating='post', maxlen=10))
inputs.append(tf.keras.preprocessing.sequence.pad_sequences(
    df_seq['categoryid'].values.tolist(), padding='post', truncating='post', maxlen=10))


def create_list(df, user_index_col, sort_col, target_col, user_num):
    """
    :param user_index_col: 用户ID列
    :param sort_col: sort含有将被用于
    :param target_col: sort你想做的栏目
    :param user_num: 用户数（从编码器等处获得）
    """
    inputs = [[] for _ in range(user_num)]
    for _, user_index, sort_value, target_value in df[[user_index_col, sort_col, target_col]].itertuples():
        inputs[user_index].append([target_value, sort_value])

    return inputs


itemid_inputs = create_list(df, user_index_col='userid', sort_col='timestamp', target_col='itemid', user_num=3)
categoryid_inputs = create_list(df, user_index_col='userid', sort_col='timestamp', target_col='categoryid', user_num=3)

print('itemid')
pprint.pprint(itemid_inputs)

print('categoryid')
pprint.pprint(categoryid_inputs)

def sort_list(inputs, is_descending):
    """
    :param is_descending: 降序或不降序
    """
    return [sorted(i_input, key=lambda i: i[1], reverse=is_descending) for i_input in inputs]


itemid_inputs = sort_list(itemid_inputs, is_descending=False)
categoryid_inputs = sort_list(categoryid_inputs, is_descending=False)

print('itemid')
pprint.pprint(itemid_inputs)

print('categoryid')
pprint.pprint(categoryid_inputs)

def create_sequential(inputs):
    # 从列表中删除时间戳的列表
    return [[i[0] for i in i_input] for i_input in inputs]

print('每个用户接触过的项目ID（按时间顺序排列）')
pprint.pprint(create_sequential(itemid_inputs))

print('每个用户联系过的类别id（按时间顺序排列）')
pprint.pprint(create_sequential(categoryid_inputs))

def create_category(inputs, n=-1):
    """
    :param n: 按时间顺序排列的名单中，有多少人被保留下来
    """
    # 从列表中删除时间戳的列表
    # 只保留时间序列中第n个序列数据的顺序
    return [[i[0] for i in i_input][n] for i_input in inputs]

print('每个用户联系的最新项目ID')
pprint.pprint(create_category(itemid_inputs, -1))

print('每个用户联系的最新类别id')
pprint.pprint(create_category(categoryid_inputs, -1))


def create_features(
        df, user_index_col, sort_col, target_col, user_num, is_descending, is_sequence, n=-1):
    """
    :param user_index_col: 用户ID列
    :param sort_col: sort含有将被用于
    :param target_col: sort你想做的栏目
    :param user_num: 用户数（从编码器等处获得）
    :param is_descending: 降序或不降序
    :param is_sequence: 有无顺序
    :param n: 有多少按时间顺序排列的清单被保存下来（仅有类别）
    """
    # 创建一个列表
    inputs = [[] for _ in range(user_num)]
    for _, user_index, sort_value, target_value in df[[user_index_col, sort_col, target_col]].itertuples():
        inputs[user_index].append([target_value, sort_value])

    # 列表排序
    inputs = [sorted(i_input, key=lambda i: i[1], reverse=is_descending) for i_input in inputs]

    if is_sequence:
        return [[i[0] for i in i_input] for i_input in inputs]
    else:
        return [[i[0] for i in i_input][n] for i_input in inputs]

print(create_features(df, user_index_col='userid', sort_col='timestamp', target_col='itemid', user_num=3, is_descending=False, is_sequence=True))
print(create_features(df, user_index_col='userid', sort_col='timestamp', target_col='itemid', user_num=3, is_descending=False, is_sequence=False))

# 例示用
df1 = df[:7]
df2 = df[7:14]
df3 = df[14:21]

print(df1)
print(df2)
print(df3)

df_dict = {}
df_dict['df1'] = df1
df_dict['df2'] = df2
df_dict['df3'] = df3

pprint.pprint(df_dict)

def create_features_by_datasets(
        df_dict, user_index_col, sort_col, target_col, user_num, is_descending, is_sequence, n=-1):
    inputs = [[] for _ in range(user_num)]

    # 对数据集分区的每个单元进行处理
    for df in df_dict.values():
        for _, user_index, sort_value, target_value in df[[user_index_col, sort_col, target_col]].itertuples():
            inputs[user_index].append([target_value, sort_value])

    inputs = [sorted(i_input, key=lambda i: i[1], reverse=is_descending) for i_input in inputs]

    if is_sequence:
        return [[i[0] for i in i_input] for i_input in inputs]
    else:
        return [[i[0] for i in i_input][n] for i_input in inputs]

pprint.pprint(create_features_by_datasets(df_dict, user_index_col='userid', sort_col='timestamp', target_col='itemid', user_num=3, is_descending=False, is_sequence=True))
pprint.pprint(create_features_by_datasets(df_dict, user_index_col='userid', sort_col='timestamp', target_col='itemid', user_num=3, is_descending=False, is_sequence=False))


data = {}
data['userid'] = np.random.randint(0, 3, (21,))
data['itemid'] = np.random.randint(0, 10, (21,))
data['score'] = np.random.rand(21)

df = pd.DataFrame(data=data)


data_cate = {}
data_cate['itemid'] = np.array([0,1,2,3,4,5,6,7,8,9,10])
data_cate['categoryid'] = np.array([0,0,0,1,1,1,2,2,2,3,3])
df_cate = pd.DataFrame(data=data_cate)
df = pd.merge(df, df_cate, how='left', on='itemid')
df = df[['userid','itemid','categoryid','score']]
df = df.sort_values(by=['userid','itemid']).reset_index(drop=True)
print('例示用')
print(df)

print('得分顺序（itemid）')
pprint.pprint(create_features(df, user_index_col='userid', sort_col='score', target_col='itemid', user_num=3, is_descending=True, is_sequence=True))
print('最高分（itemid）')
pprint.pprint(create_features(df, user_index_col='userid', sort_col='score', target_col='itemid', user_num=3, is_descending=True, is_sequence=False, n=0))



#https://nnkkmto.hatenablog.com/entry/2019/12/02/193702
