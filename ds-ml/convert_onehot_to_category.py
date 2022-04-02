import pandas as pd
import numpy as np

df = pd.DataFrame(columns=['movie_id', 'genre'])
df['movie_id'] = np.array([1, 2, 2, 3, 3, 4, 5, 5, 5])
df['genre'] = np.array(['action', 'romance', 'action', 'sf', 'action', 'horror', 'sf', 'horror', 'action'])
print(df)

df_onehot = pd.get_dummies(df['genre'])
df_onehot = pd.concat([df[['movie_id']], df_onehot], axis=1)
print(df_onehot)


def convert_onehot_to_category(df, id_col, one_hot_columns, category_col='category'):
    df_concat = pd.DataFrame(columns=[id_col, category_col])
    for col in one_hot_columns:
        # 只留下那些数值为1或以上的。
        df_each = df[df[col] >= 1][[id_col, col]]
        # 用类别值替换数值。
        df_each[col] = col

        df_each.columns = [id_col, category_col]
        df_concat = pd.concat([df_concat, df_each], axis=0)

    # 重複削除
    df_concat = df_concat.drop_duplicates().reset_index(drop=True).sort_values(by=id_col)
    return df_concat


genres = ['action', 'romance', 'sf', 'horror']
id_col = 'movie_id'
category_col = 'genre'

df_category = convert_onehot_to_category(df_onehot, id_col=id_col, one_hot_columns=genres, category_col=category_col)

print(df_category)
