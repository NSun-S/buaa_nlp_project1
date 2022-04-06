import jieba
from dataPrepare import *


def calculate_entropy(tf_dic, len_data):
    """
    计算一元词的信息熵
    :return:
    """
    begin = time.time()
    words_num = sum([item[1] for item in tf_dic.items()])

    print("分词个数：{}".format(words_num))
    print('不同词个数：{}'.format((len(tf_dic))))
    print("平均词长：{:.6f}".format(len_data/float(words_num)))

    entropy = 0
    for item in tf_dic.items():
        entropy += -(item[1]/words_num) * math.log(item[1]/words_num, 2)
    print("基于分词的一元模型中文信息熵为：{:.6f} 比特/词".format(entropy))

    end = time.time()
    print("一元模型运行时间：{:.6f} s".format(end - begin))
    return ['unigram', len_data, words_num, round(len_data/float(words_num), 6), round(entropy, 6)]


def calculate_bigram_entropy(tf_dic, bigram_tf_dic, len_data):
    """
    计算二元词的信息熵
    :return:
    """
    begin = time.time()
    bi_words_num = sum([item[1] for item in bigram_tf_dic.items()])
    avg_word_len = sum(len(item[0][i]) for item in bigram_tf_dic.items() for i in range(len(item[0]))) / bi_words_num

    print("分词个数：{}".format(bi_words_num))
    print('不同词个数：{}'.format((len(bigram_tf_dic))))
    print("平均词长：{:.6f}".format(avg_word_len))

    entropy = 0
    for bi_item in bigram_tf_dic.items():
        jp = bi_item[1] / bi_words_num
        cp = bi_item[1] / tf_dic[bi_item[0][0]]
        entropy += -jp * math.log(cp, 2)
    print("基于分词的二元模型中文信息熵为：{:.6f} 比特/词".format(entropy))

    end = time.time()
    print("二元模型运行时间：{:.6f} s".format(end - begin))
    return ['bigram', len_data, bi_words_num, round(avg_word_len, 6), round(entropy, 6)]


def calculate_trigram_entropy(bigram_tf_dic, trigram_tf_dic, len_data):
    """
    计算三元词的信息熵
    :return:
    """
    begin = time.time()
    tri_words_num = sum([item[1] for item in trigram_tf_dic.items()])
    avg_word_len = sum(len(item[0][i]) for item in trigram_tf_dic.items() for i in range(len(item[0])))/tri_words_num

    print("分词个数：{}".format(tri_words_num))
    print('不同词个数：{}'.format((len(trigram_tf_dic))))
    print("平均词长：{:.6f}".format(avg_word_len))

    entropy = 0
    for tri_item in trigram_tf_dic.items():
        jp = tri_item[1] / tri_words_num
        cp = tri_item[1] / bigram_tf_dic[tri_item[0][0]]
        entropy += -jp * math.log(cp, 2)
    print("基于分词的三元模型中文信息熵为：{:.6f} 比特/词".format(entropy))

    end = time.time()
    print("三元模型运行时间：{:.6f} s".format(end - begin))
    return ['trigram', len_data, tri_words_num, round(avg_word_len, 6), round(entropy, 6)]


def calculate(data):
    split_words = list(jieba.cut(data))
    words_num = len(split_words)
    print("语料库字数：{}".format(len(data)))
    # b = time.time()
    # print('语料库加载时间：{:.6f} s'.format(b - a))
    tf_dic = {}
    bigram_tf_dic = {}
    trigram_tf_dic = {}
    get_tf(tf_dic, split_words)
    get_bigram_tf(bigram_tf_dic, split_words)
    get_trigram_tf(trigram_tf_dic, split_words)

    rows = []
    print('---------------------------------')
    rows.append(calculate_entropy(tf_dic, len(data)))
    print('---------------------------------')
    rows.append(calculate_bigram_entropy(tf_dic, bigram_tf_dic, len(data)))
    print('---------------------------------')
    rows.append(calculate_trigram_entropy(bigram_tf_dic, trigram_tf_dic, len(data)))
    return rows


def calculate_inf_entropy(inf):
    """
    计算一系列文件的信息熵
    :param inf:要求解信息熵的索引文件 ，文件内容为文件名，以','分隔
    :return:
    """
    # a = time.time()
    data = get_all_corpus(inf)
    rows = calculate(data)
    head = "#"
    row_title = [str(i + 1) for i in range(len(rows))]
    col_title = ['分词模型', '语料字数', '分词个数', '平均词长', '信息熵（比特/词）']
    print_md('金庸小说全集（16本）信息熵表', head, row_title, col_title, rows)


def calculate_dir_entropy():
    """
    计算DATA_PATH下每个文件单独的信息熵
    :return:
    """
    rows = []
    for file in os.listdir(DATA_PATH):
        print("\n当前计算信息熵的文件为：{}".format(file))
        file_path = DATA_PATH + file
        data = get_single_corpus(file_path)
        temp_rows = calculate(data)
        rows.append([file.split('.')[0], temp_rows[0][1], temp_rows[0][2], temp_rows[0][3], temp_rows[0][4],
                     temp_rows[1][2], temp_rows[1][3], temp_rows[1][4],
                     temp_rows[2][2], temp_rows[2][3], temp_rows[2][4]])
    head = '#'
    row_title = [str(i + 1) for i in range(len(rows))]
    col_title = ['小说名', '语料字数', '一元分词个数', '一元平均词长', '一元模型信息熵（比特/词）', '二元分词个数', '二元平均词长', '二元模型信息熵（比特/词）',
                 '三元分词个数', '三元平均词长', '三元模型信息熵（比特/词）']
    print_md('金庸小说全集（16本）信息熵表', head, row_title, col_title, rows)


if __name__ == "__main__":
    # calculate_inf_entropy('../inf.txt')
    calculate_dir_entropy()
