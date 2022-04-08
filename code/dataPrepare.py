import os
import re
import math
import time
import jieba

DATA_PATH = '../jyxstxtqj/'


def get_single_corpus(file_path):
    """
    获取file_path文件对应的内容
    :return: file_path文件处理结果
    """
    corpus = ''
    # unuseful items filter
    r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:：;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~「」『』（）]+'
    with open(file_path, 'r', encoding='ANSI') as f:
        corpus = f.read()
        corpus = re.sub(r1, '', corpus)
        corpus = corpus.replace('\n', '')
        corpus = corpus.replace('\u3000', '')
        corpus = corpus.replace('本书来自免费小说下载站更多更新免费电子书请关注', '')
        f.close()
    return corpus


def get_all_corpus(index_file):
    """
    获取所有语料库文件的内容列表
    :return: 全部txt文件处理结果
    """
    index_path = index_file
    whole_corpus = []
    with open(index_path, 'r') as f:
        txt_list = f.readline().split(',')
        print("要求解信息熵的文件列表为：")
        for file in txt_list:
            print(file)
            file_path = DATA_PATH + file + '.txt'
            whole_corpus.append(get_single_corpus(file_path))
        print('---------------------------')
        f.close()
    return ''.join(whole_corpus)


def get_tf(tf_dic, words):
    """
    获取一元词词频
    :return:一元词词频dic
    """
    for i in range(len(words)):
        tf_dic[words[i]] = tf_dic.get(words[i], 0) + 1


def get_bigram_tf(tf_dic, words):
    """
    获取二元词词频
    :return:二元词词频dic
    """
    for i in range(len(words)-1):
        tf_dic[(words[i], words[i+1])] = tf_dic.get((words[i], words[i+1]), 0) + 1


def get_trigram_tf(tf_dic, words):
    """
    获取三元词词频
    :return:三元词词频dic
    """
    for i in range(len(words)-2):
        tf_dic[((words[i], words[i+1]), words[i+2])] = tf_dic.get(((words[i], words[i+1]), words[i+2]), 0) + 1


def print_md(table_name, head, row_title, col_title, data):
    """
    :param table_name: 表名
    :param head: 表头
    :param row_title: 行名，编号，1，2，3……
    :param col_title: 列名，词数，运行时间等
    :param data: {ndarray(H, W)}
    :return:字符串形式的markdown表格
    """
    element = " {} |"

    h, w = len(data), len(data[0])
    lines = ['#### {}'.format(table_name)]

    lines += ["| {} | {} |".format(head, ' | '.join(col_title))]

    # 分割线
    split = "{}:{}"
    line = "| {} |".format(split.format('-' * len(head), '-' * len(head)))
    for i in range(w):
        line = "{} {} |".format(line, split.format('-' * len(col_title[i]), '-' * len(col_title[i])))
    lines += [line]

    # 数据部分
    for i in range(h):
        d = list(map(str, list(data[i])))
        lines += ["| {} | {} |".format(row_title[i], ' | '.join(d))]

    table = '\n'.join(lines)
    print(table)
    return table


if __name__ == '__main__':
    # calculate_inf_entropy('inf.txt')
    pass

