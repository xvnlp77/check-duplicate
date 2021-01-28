"""
@Author  : chouxiaohui
@Date    : 2021/1/23 11:50 上午
@Version : 1.0
"""
import re
import jieba
import jieba.analyse
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer


def filter_html(content):
    """去除网页标签"""
    return re.sub(r'<[^>]*>', '', content)


def filter_punctuation(content):
    """去除标点符号"""
    punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~“”？，！【】（）、。：；’‘……￥·"""
    # return re.sub(r'[^\w\s]', '', content)
    return re.sub(punctuation, '', content)


def split_sentence(content):
    """拆分句子"""
    punctuation = r"""[!,.:;?~“”？，！。：；’‘……]"""
    sentences = re.split(punctuation, content)
    return sentences


# def count_1_gram(sentences):
#     """统计一元字/词"""
#     char_num_dict = {}
#     for c in sentences:
#         if c in char_num_dict:
#             char_num_dict[c] += 1
#         else:
#             char_num_dict[c] = 1
#     print(char_num_dict)
#     print(len(char_num_dict))
#     return char_num_dict


def count_n_gram(sentences, ngram_range=(2, 2)):
    """统计N元字/词"""
    char_num_dict = {}
    vectorizer = CountVectorizer(analyzer='word', token_pattern=u"(?u)\\b\\w+\\b", ngram_range=ngram_range)
    X = vectorizer.fit_transform(sentences)
    nums = np.sum(X.toarray(), axis=0)
    # print(vectorizer.get_feature_names())
    # print(nums)
    # print(len(vectorizer.get_feature_names()))
    for key, num in zip(vectorizer.get_feature_names(), nums):
        char_num_dict[key] = num
    return char_num_dict


def compute_by_n_gram(c_1, c_2, ngram_range=(1, 1)):
    """基于N元字/词计算"""
    c1_num_dict = count_n_gram(c_1, ngram_range)
    c2_num_dict = count_n_gram(c_2, ngram_range)
    duplicate_char_rate = {}
    for char1, num1 in c1_num_dict.items():
        if char1 in c2_num_dict:
            num2 = c2_num_dict[char1]
            denominator = num1 if num1 > num2 or num1 == num2 else num2
            molecular = num1 if num1 < num2 else num2
            rate = molecular / denominator
            duplicate_char_rate[char1] = rate

    # unique_char_num = len(c1_num_dict) + len(c2_num_dict) - len(duplicate_char_rate)
    return duplicate_char_rate, len(c1_num_dict), len(c2_num_dict)


def compute_by_n_gram_2(c_1, c_2, ngram_range=(1, 1)):
    """基于N元字/词计算"""
    c1_num_dict = count_n_gram(c_1, ngram_range)
    c2_num_dict = count_n_gram(c_2, ngram_range)
    same_num = 0.0
    for char1, num1 in c1_num_dict.items():
        if char1 in c2_num_dict:
            num2 = c2_num_dict[char1]
            each_same_num = num1 if num1 < num2 or num1 == num2 else num2
            same_num += each_same_num

    return same_num,sum(c1_num_dict.values()),sum(c2_num_dict.values())


def compute_duplicate_rate(content_1, content_2):
    """计算重复率"""
    content_1 = filter_html(content_1.replace(' ',''))
    # content_1 = filter_punctuation(content_1)

    content_2 = filter_html(content_2.replace(' ',''))
    # content_2 = filter_punctuation(content_2)
    # duplicate_char_rate, c1_len, c2_len = compute_by_n_gram(content_1, content_2)

    # 基于字
    c_1 = ' '.join(list(content_1))
    c_2 = ' '.join(list(content_2))
    s_1 = split_sentence(c_1)
    s_2 = split_sentence(c_2)

    # 一元
    duplicate_char_rate, c1_len, c2_len = compute_by_n_gram(s_1, s_2, ngram_range=(1, 1))
    # 二元
    # duplicate_char_rate, c1_len, c2_len = compute_by_n_gram(s_1, s_2, ngram_range=(2, 2))

    # # 基于词
    # c_1 = ' '.join(list(jieba.cut(content_1)))
    # c_2 = ' '.join(list(jieba.cut(content_2)))
    # # print(c_1)
    # s_1 = split_sentence(c_1)
    # s_2 = split_sentence(c_2)
    # # print(s_1)
    # # 一元
    # # duplicate_char_rate, c1_len, c2_len = compute_by_n_gram(s_1, s_2, ngram_range=(1, 1))
    # # 二元
    # duplicate_char_rate, c1_len, c2_len = compute_by_n_gram(s_1, s_2, ngram_range=(2, 2))

    total_rate = 0.0
    for char, rate in duplicate_char_rate.items():
        total_rate += rate
    c1_duplicate_rate = total_rate / c1_len
    c2_duplicate_rate = total_rate / c2_len
    return c1_duplicate_rate, c2_duplicate_rate


def compute_duplicate_rate_2(content_1, content_2):
    """相同字符数/全部字符"""
    content_1 = filter_html(content_1)
    # content_1 = filter_punctuation(content_1)

    content_2 = filter_html(content_2)
    # content_2 = filter_punctuation(content_2)
    # duplicate_char_rate, c1_len, c2_len = compute_by_n_gram(content_1, content_2)

    # 基于字
    # c1 = list(content_1)
    # c2 = list(content_2)
    # c_1 = ' '.join(c1)
    # c_2 = ' '.join(c2)
    # s_1 = split_sentence(c_1)
    # s_2 = split_sentence(c_2)

    # 一元
    # same_num = compute_by_n_gram_2(s_1, s_2, ngram_range=(1, 1))
    # 二元
    # same_num = compute_by_n_gram_2(s_1, s_2, ngram_range=(2, 2))

    # 基于词
    c1 = list(jieba.cut(content_1))
    c2 = list(jieba.cut(content_2))

    c_1 = ' '.join(c1)
    c_2 = ' '.join(c2)
    # print(c_1)
    s_1 = split_sentence(c_1)
    s_2 = split_sentence(c_2)
    # print(s_1)
    # 一元
    same_num,c1_len,c2_len = compute_by_n_gram_2(s_1, s_2, ngram_range=(1, 1))
    # 二元
    # same_num = compute_by_n_gram_2(s_1, s_2, ngram_range=(2, 2))

    # print('相同字符数：', str(same_num))
    # print('第一篇字符数：', str(c1_len))
    # print('第二篇字符数：', str(c2_len))

    return same_num / c1_len, same_num / c2_len


def get_keywords(content):
    keywords = jieba.analyse.textrank(content, topK=100)
    return keywords


if __name__ == '__main__':
    # c1 = "【#国家卫健委再次回应春节返乡问题#】①《冬春季农村地区新冠肺炎疫情防控工作方案》中返乡人员是指从外地返回农村地区的人员，需要持核酸检测阴性证明返乡，并进行14天居家健康监测，返回城市人员需遵守目的地疫情防控要求；②1月28日后返乡人员，须在返乡后第7天和第14天分别做一次核酸检测，1月28日之前返乡人员是否需核酸检测以目的地要求为准；③#居家健康监测不是居家隔离#而是做好体温与症状监测，非必要不外出；④网格化管理是指将农村划分为若干网格，村委会人员等各方力量，以网格为单位，分片包干，对返乡人员做好摸排登记、健康监测、宣传教育等工作。（记者彭韵佳）"
    # c2 = "【#国家卫健委再次回应春节返乡问题#】①《冬春季农村地区新冠肺炎疫情防控工作方案》中返乡人员是指从外地返回农村地区的人员，需要持核酸检测阴性证明返乡，并进行14天居家健康监测，返回城市人员需遵守目的地疫情防控要求；②1月28日后返乡人员，须在返乡后第7天和第14天分别做一次核酸检测，1月28日之前返乡人员是否需核酸检测以目的地要求为准；③#居家健康监测不是居家隔离#而是做好体温与症状监测，非必要不外出；④网格化管理是指将农村划分为若干网格，村委会人员等各方力量，以网格为单位，分片包干，对返乡人员做好摸排登记、健康监测、宣传教育等工作。（记者彭韵佳）"

    # c2 = "【#国家卫健委再次回应春节返乡问题#冠肺炎疫情防控工作方案》中返乡人员是指从外地返回农村地区的人员，需要持核酸检测阴性证明返乡，并进行14天居家健康监测，返回城市人员需遵守目的地疫情防控要求；②1月28日后返乡人员，须在返乡后第7天和第14天分别做一次核酸检测，1月28日之前返乡人员是否需核酸检测以目的地要求为准；③#居家健康监测不是居家隔离#而是做好体温与症状监测，非必要不外出；④网格化管理是指将农村划分为若干网格，村委会人员等各方力量，以网格为单位，分片包干，对返乡人员做好摸排登记、健康监测、宣传教育等工作。（记者彭韵佳）"
    # c2 = "为做好冬春季农村地区新冠肺炎疫情防控工作，方案自下发之日开始执行。持核酸检测阴性证明返乡从1月28日春运开始后实施，至3月8日春运结束后截止。方案规定“持核酸检测阴性证明返乡后不需要隔离，但需要进行14天居家健康监测”，是不是返回城市就不要落实14天居家健康监测？方案所指返乡人员是指从外地返回农村地区的人员，需要持核酸检测阴性证明返乡，并进行14天居家健康监测，返回城市人员需遵守目的地疫情防控要求。■ 方案中提到的居家监测与隔离有什么区别？居家健康监测，要求做好体温、症状监测，非必要不外出。如果出现发热、干咳、咽痛、嗅（味）觉减退、腹泻等身体不适症状，及时到医院就诊。居家隔离，要求在社区医务人员指导下，单独居住，不能外出。"

    c1 = "111211"
    c2 = "111221"

    duplicate_rate = compute_duplicate_rate_2(c1, c2)
    print(duplicate_rate)

    # print(get_keywords(c1))
    # print(get_keywords(c2))

    # k1 = get_keywords(c1)
    # k2 = get_keywords(c2)
    # set_all = set(k1).intersection(set(k2))

    # print(k1)
    # print(k2)
    # print(set_all)
    # print(len(set_all) / len(k1))
    # print(len(set_all) / len(k2))

# 指标
