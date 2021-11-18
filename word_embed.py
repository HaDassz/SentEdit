# %%
import os
import re
import gensim
import json
import requests as req

HANZI_RANGE = u"[\u4E00-\u9FFF]"
NOT_PUNCTUATION = u"[^\u0021-\u002F\u003A-\u0040\u005B-\u0060\u007B-\u007E~!@#$%^&*()_+=\-`\[\]{}';:\".,<>/?\|，。；：！？（）＼｜【】《》」「]"
CORPUS_NAME = {'YL_V1': '遠流語料', 'CP_V1': '中國時報', 'MDN': '國語日報',
               'SBCV1': '平衡語料庫', 'cna': 'Chinese Giga Words'}
LIMIT_WORD_LEVEL = {float("inf"):"不限制", 1.0:"1級詞", 2.0:"2級詞以下", 3.0:"3級詞以下", 4.0:"4級詞以下", 5.0:"5級詞以下", 6.0:"6級詞以下",\
                    7.0:"7級詞以下"}

# PUNCTUATION = u"[\u0021-\u002F\u003A-\u0040\u005B-\u0060\u007B-\u007E，。；：！？（）＼｜【】]"
config_path = os.path.abspath(os.path.dirname(__file__))
patt = re.compile(NOT_PUNCTUATION)
# patt_punct = re.compile(PUNCTUATION)

with open(os.path.join(config_path, 'sentedit', '國教院詞語分級表.json'), encoding="utf-8") as fin:
    level_data = json.loads(fin.read())


def select_model(model_name='MDN'):
    """根據model_name選擇載入的二進位模型

    :param model_fname: [模型檔名]
    :type model_fname: [str]
    :return embed_model: [gensim.models.KeyedVectors]
    """
    model_map = {'YL_V1': 'YL_V1.bin', 'CP_V1': 'CP_V1.bin', 'MDN': 'MDN.bin', 'SBCV1': 'SBCV1.bin', 'cna': 'cna_asbc_concat_vectors.bin'}
    embed_model = gensim.models.keyedvectors.KeyedVectors.load_word2vec_format(os.path.join(config_path, 'nlpmodels', model_map.get(model_name)),\
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

# TODO: 110/10/22 詢問說要不要判斷近義詞的級數，只供原詞語等級以下的詞語才能被選擇(完成)
# TODO: 110/11/2 開始寫供使用者填顯示詞語的等級

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







def segStr_with_naerSeg(sentence):
    """傳POST請求到國教院分詞系統再取得分詞後字串

    :param sentence: [需要分詞的字串]
    :type sentence: [str]
    :return seg_str: [分詞完的字串，用半形空格分隔]
    """
    json_str = json.dumps({"RawText":sentence, "withPOS":"without"})
    headers = {'user-agent': 'Mozilla/5.0'}
    r = req.post(url="https://coct.naer.edu.tw/Segmentor/Func/getSegResult/", data=json_str, headers=headers)
    seg_lst = json.loads(r.text)["result"]
    res_lst = [word_POS[0] for word_POS in seg_lst]
    seg_str = " ".join(res_lst)
    return seg_str

# print(segStr_with_naerSeg("好朋友買了好幾件衣料，綠色的底子帶粉紅色圓圈，當她拿給我們看時，一位對圍棋十分感興趣的同學指出：「啊，好像棋盤似的。」"))


