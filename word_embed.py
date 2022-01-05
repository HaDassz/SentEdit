# %%
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   word_embed.py
@Time    :   2022/01/05 15:21:09
@Author  :   cwHsu 
@Version :   1.0
@Contact :   old90631@mail.naer.edu.tw
@License :   None
@Desc    :   運用詞嵌入(word embedding)技術找出語義場關聯詞，並根據詞表提供適當的資訊給前端處理。
'''

import os
import re
import gensim
import json

HANZI_RANGE = u"[\u4E00-\u9FFF]"
NOT_PUNCTUATION = u"[^\u0021-\u002F\u003A-\u0040\u005B-\u0060\u007B-\u007E~!@#$%^&*()_+=\-`\[\]{}';:\".,<>/?\|，。；：！？（）＼｜【】《》」「]"
CORPUS_NAME = {'YL_V1': '遠流語料', 'CP_V1': '中國時報', 'MDN': '國語日報',
               'SBCV1': '平衡語料庫', 'cna': 'Chinese Giga Words'}
LIMIT_WORD_LEVEL = {float("inf"): "不限制", 1.0: "1級詞", 2.0: "2級詞以下", 3.0: "3級詞以下", 4.0: "4級詞以下", 5.0: "5級詞以下", 6.0: "6級詞以下",
                    7.0: "7級詞以下"}

config_path = os.path.abspath(os.path.dirname(__file__))
patt = re.compile(NOT_PUNCTUATION)

with open(os.path.join(config_path, 'sentedit', '國教院詞語分級表.json'), encoding="utf-8") as fin:
    level_data = json.loads(fin.read())


def select_model(model_name='MDN'):
    """根據model_name選擇載入的二進位模型

    :param model_fname: [模型檔名]
    :type model_fname: [str]
    :return embed_model: [gensim.models.KeyedVectors]
    """
    model_map = {'YL_V1': 'YL_V1.bin', 'CP_V1': 'CP_V1.bin', 'MDN': 'MDN.bin',
                 'SBCV1': 'SBCV1.bin', 'cna': 'cna_asbc_concat_vectors.bin'}
    embed_model = gensim.models.keyedvectors.KeyedVectors.load_word2vec_format(os.path.join(config_path, 'nlpmodels', model_map.get(model_name)),
                                                                               binary=True, encoding='utf8', unicode_errors='ignore')
    return embed_model


def judge_word_level(word):
    word_level_lst = level_data.get(word, "此詞語不存在於分級表")
    if word_level_lst == "此詞語不存在於分級表":
        return float("inf")
    else:
        return float(word_level_lst[0][0])


def stringfy_word_level(word):
    word_level_lst = level_data.get(word, "此詞語不存在於分級表")
    if word_level_lst == "此詞語不存在於分級表":
        return "X"
    else:
        res = [str(lst[0]) for lst in word_level_lst]
        return ",".join(res)


def find_most_n_similar(w1, model, topn=10, limit_word_level=float("inf")):
    if model.has_index_for(w1):
        # w1_level = judge_word_level(
        #     w1) if limit_word_level else float("inf")
        result_lst = model.most_similar(w1, topn=topn)
        temp_lst = [stringfy_word_level(word) + ' ' + word + ' ' + str(round(cos_sim, 2)) for word, cos_sim in result_lst
                    if (judge_word_level(word) <= limit_word_level)]
        return '\n'.join(temp_lst) if (temp_lst != []) else (stringfy_word_level(w1) + ' ' + w1)
    else:
        return stringfy_word_level(w1) + ' ' + w1


def judgeWordLevel_to_dict(word):
    word_level_lst = level_data.get(word, "此詞語不存在於分級表")
    if word_level_lst == "此詞語不存在於分級表":
        return {
            "className": "level_X",
            "title": "未收錄",
            "levelNum": "X"
        }
    else:
        level_lst = level_data[word]
        title_str_lst = []
        level_num_lst = []
        for arr in level_lst:
            title_str_lst.append(arr[0] + "," + arr[1])
            level_num_lst.append(arr[0])
        return {
            "className": "level_" + level_lst[0][0],
            "title": "； ".join(title_str_lst),
            "levelNum": ",".join(level_num_lst)
        }