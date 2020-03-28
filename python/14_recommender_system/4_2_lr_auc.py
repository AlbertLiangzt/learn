#!/usr/local/python/bin
# --coding:utf-8--

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

input_file = "./data/4_1_samples.data"
output_true_label_file = "./data/4_2_True_label.data"
output_pre_label_file = "./data/4_2_Predict_label.data"
output_auc_data = "./data/4_2_auc.data"
output_model_w = "./data/4_2_model.w"
output_model_b = "./data/4_2_model.b"

# label	gender:weight_1	age:weight_2	token_1:score_1	token_2:score_2
def load_data():
    label_list = []  # 每个样本的label标签
    fea_row_list = []  # 样本行信息
    fea_col_list = []  # 样本列信息
    data_list = []  # 存储真实数据

    row_index = 0
    max_col = 0

    with open(input_file, "r") as fd:
        for line in fd:
            sample = line.strip().split(" ")
            label = sample[0]
            features = sample[1:]

            label_list.append(label)

            for fea_score in features:
                ss = fea_score.strip().split(":")

                if len(ss) != 2:
                    continue
                feature, score = ss

                fea_row_list.append(row_index)
                fea_col_list.append(feature)
                data_list.append(float(score))

                if int(feature) > max_col:
                    max_col = int(feature)
            row_index += 1

    row = np.array(fea_row_list)
    col = np.array(fea_col_list)
    data = np.array(data_list)

    fea_datasets = csr_matrix((data, (row, col)), shape=(row_index, max_col + 1))
    # 分割训练集和测试集
    # 原始数据、真实标签、 样本占比、随机数种子
    x_train, x_test, y_train, y_test = train_test_split(fea_datasets, label_list, test_size=0.2, random_state=0)
    return x_train, x_test, y_train, y_test


def main():
    x_train, x_test, y_train, y_test = load_data()
    model = LogisticRegression(penalty='l1')
    model.fit(x_train, y_train)

    ff_w = open(output_model_w, 'w')
    ff_b = open(output_model_b, 'w')

    for w_list in model.coef_:
        for w in w_list:
            print >> ff_w, "w: ", w

    for b in model.intercept_:
        print >> ff_b, "b: ", b

    # print "w: ", model.coef_
    # print "b: ", model.intercept_
    print "precision: ", model.score(x_test, y_test)
    # print "MSE: ", np.mean((model.predict(x_test) - y_test) ** 2)

    ff_t = open(output_true_label_file, 'w')
    ff_p = open(output_pre_label_file, 'w')

    # 输出真实label和预测label，到两个不同的文件中
    for y in y_test:
        print >> ff_t, y

    for y in model.predict_proba(x_test):
        print >> ff_p, y


# 将刚生成的两个文件合并成auc文件
def merge_as_auc():
    t_list = []
    for line in (open(output_true_label_file, 'r')):
        t_list.append(line)

    p_list = []
    for line in (open(output_pre_label_file, 'r')):
        ss = line.strip().split()[1][:-1]
        p_list.append(ss)

    ff_s = open(output_auc_data, 'w')
    a = 0
    for idx in t_list:
        left = str(t_list[a]).strip()
        right = str(p_list[a]).strip()
        ff_s.write("\t".join([str(left), str(right)]))
        ff_s.write("\n")
        a += 1
    ff_s.close()


if __name__ == "__main__":
    main()
    merge_as_auc()
