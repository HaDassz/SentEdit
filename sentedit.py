#!/usr/bin/python
# -*- encoding: UTF-8 -*-

import os
import json
import re
# import string
from Segmentor import *
from collections import OrderedDict, defaultdict
import gensim
from word_embed import select_model, find_most_n_similar, judgeWordLevel_to_dict, stringfy_word_level

config_path = os.path.abspath(os.path.dirname(__file__))

class WordLevelTagger:
    def __init__(self):
        self.ws=Segmentor()
        self.WordTableFiles = OrderedDict([(
            'hw8000',
            [
                u'華語八千詞',
                'sentedit/華語八千詞分級.json',
                [u"準備一級", u"準備二級", u"入門級", u"基礎級", u"進階級", u"高階級", u"流利級"]
            ]
        ), (
            'naer',
            [
                u'國教院詞語分級表',
                'sentedit/國教院詞語分級表.json',
                [u"基礎", u"基礎", u"基礎", u"進階", u"進階", u"精熟", u"精熟"]
            ]
        )])
        self.WordTables = {}
        for k, v in self.WordTableFiles.items():
            self.WordTables[k] = {
                'name': v[0],
                'dict': json.load(open(v[1], encoding="utf-8")),
                'level_info': v[2]
            }
        # print json.dumps(self.WordTables, ensure_ascii=False).encode("UTF-8")

    def get_dicts(self):
        L = []
        for k, v in self.WordTables.items():
            L.append((k, v['name']))
        return L

    def tag(self, table_id, text, wordseg, corpus, limitWordLv, topn):
        level_stats = defaultdict(int)
        table_name = self.WordTables[table_id]['name']
        level_info = self.WordTables[table_id]['level_info']
        word_listT = defaultdict(int)
        embed_model = select_model(corpus)
        T = self.WordTables[table_id]['dict']
        # print json.dumps(T,ensure_ascii=False,indent=4).encode("UTF-8")
        if wordseg:
            sentL = []
            for sent in re.split('[\r\n]', text):
                # wL = self.seg_by_naerSeg(sent)
                wL = self.ws.segment(sent)
                # print json.dumps(wL,ensure_ascii=False).encode("utf8")
                wL1 = []
                for w in wL:
                    L = re.findall(u'([。，；！？：「」]|[^。，；！？：「」]+)', w)
                    wL1 += L
                sentL.append(wL1)
        else:
            sentL = []
            for sent in re.split('[\r\n]', text):
                sentL.append(re.split('[ \t]+', sent))

        # 分級標記
        L = []
        for no, x in enumerate(level_info, 1):
            L.append(u"""<table class="word"><tr><td>%s</td></tr><tr><td class="level_%s"></td></tr><tr><td>%s</td></tr></table>""" % (x, no, no))

        table_info = u"""
            <button class="btn btn-outline-secondary" type="button" data-toggle="collapse" href="#collapseExample" aria-expanded="false" aria-controls="collapseExample">分級詞表：%s</button>
            <div class="collapse" id="collapseExample">
            <div>
            %s
            </div>
            </div><br>
        """ % (table_name, "&nbsp;&nbsp;".join(L))
        #  % (table_name, string.join(L, "&nbsp;&nbsp;"))   # 2.7版寫法
        # print json.dumps(sentL,ensure_ascii=False,indent=4).encode("UTF-8")

        out_text = [table_info]
        word_sim_out_lst = [table_info]
        for wordL in sentL:
            # wordL=re.split('[ \t]+',sent)
            outL = []
            similar_lst = []
            word_sim = []
            for word in wordL:
                # 分級標記
                word_listT[word] += 1
                if word in T:
                    levelL = []
                    titleL = []
                    # print "DEBUG:word=%s"%(word.encode("UTF-8"))
                    for item in T[word]:
                        # print "DEBUG1:item=%s"%(item)
                        levelL.append("%s" % (item[0]))
                        titleL.append("%s" % item[1])
                    level_stats[levelL[0]] += 1  # 以最低的級去計算
                    out = u"""<table class="word" title="%s">
                            <tr><td>%s</td></tr>
                            <tr><td class="level_%s"></td></tr>
                            <tr><td>%s</td></tr>
                            </table>""" % (",".join(titleL), word, levelL[0], ",".join(levelL)) # % (",".join(titleL), word, levelL[0], ",".join(titleL))
                            # % (string.join(titleL, ","), word, levelL[0], string.join(levelL, ","))  # 2.7版
                elif not re.match(u'[\u4E00-\u9fa5]+', word):
                    out = u"""<table class="word" title="無分級">
                            <tr><td>%s</td></tr>
                            <tr><td class="level_0"></td></tr>
                            <tr><td> </td></tr>
                            </table>""" % (word)
                else:
                    out = u"""<table class='word' title='未收錄'>
                            <tr><td>%s</td></tr>
                            <tr><td class="level_X"></td></tr>
                            <tr><td>X</td></tr>
                            </table>""" % (word)
                    level_stats['X'] += 1  # 以最低的級去計算
                outL.append(out)

                #* 語義場關聯詞
                similar_lst.append(find_most_n_similar(
                    word, embed_model, topn=topn, limit_word_level=float(limitWordLv)))

            for word, sim in zip(wordL, similar_lst):
                word_sim_dict = {}
                word_sim_dict['pure_word'] = word
                word_sim_dict['word'] = stringfy_word_level(word) + ' ' + word
                word_sim_dict['sim'] = sim.split('\n')
                word_sim.append(word_sim_dict)

            #TODO: 110/11/16 至此，接著寫html字串
            word_sim_out = u""""""
            for idx, ws in enumerate(word_sim):
                word = ws['pure_word']
                word_sim_out += u'<table class="word">\n'
                word_sim_out += u'<tr>\n'
                word_sim_out += u'<td>\n'
                word_sim_out += f'<select id="form-select-{idx+1}" class="word-select" title="{judgeWordLevel_to_dict(word)["title"]}">\n'
                word_sim_out += f'<option selected class="selectedOpt">{ws["word"]}</option>\n'
                for i, sword_similarity in enumerate(ws["sim"]):
                    word_sim_out += f'<option value="{sword_similarity}" id="opt{i}">{sword_similarity}</option>\n'
                word_sim_out += '</select>\n'
                word_sim_out += '</td>\n'
                word_sim_out += '</tr>\n'
                word_sim_out += '<tr>\n'
                word_sim_out += f'<td class="{judgeWordLevel_to_dict(word)["className"]}" title="{judgeWordLevel_to_dict(word)["title"]}" id="markLevel-{idx+1}"></td>\n'
                word_sim_out += '</tr>\n'
                word_sim_out += '<tr>\n'
                word_sim_out += f'<td id="level-num-{idx+1}">{judgeWordLevel_to_dict(word)["levelNum"]}</td>\n'
                word_sim_out += '</tr>\n'
                word_sim_out += '</table>\n'

            word_sim_out_lst.append(word_sim_out)
            out_text.append(u"&nbsp;&nbsp;".join(outL))
        # 詞表
        word_list = list(word_listT.items())
        word_list.sort(key=lambda x: x[1], reverse=True)
        word_list_out = u"""<table class="table table-sm table-hover">
  <thead>
    <tr>
      <th scope="col">詞語</th>
      <th scope="col">次數</th>
      <th scope="col">等級</th>
    </tr>
  </thead>
  <tbody>
"""
        for item in word_list:
            word = item[0]
            if word in T:
                word_list_out += u"<tr>\n"
                word_list_out += u"<td>%s</td>\n" % (word)
                word_list_out += u"<td>%s</td>\n" % (item[1])
                levelL = []
                titleL = []
                for item in T[word]:
                    levelL.append(u"%s" % (item[0]))
                    titleL.append(u"%s" % (item[1]))
                word_list_out += u"<td>%s</td>\n" % (titleL[0])
                word_list_out += u"</tr>\n"
            elif not re.match(u'[\u4E00-\u9fa5]+', word):
                # word_list_out+=u"<td>無分級</td>\n"
                pass
            else:
                word_list_out += u"<tr>\n"
                word_list_out += u"<td>%s</td>\n" % (word)
                word_list_out += u"<td>%s</td>\n" % (item[1])
                word_list_out += u"<td>未收錄</td>\n"
                word_list_out += u"</tr>\n"
        word_list_out += u"""</tbody>
</table>"""

        output = {
            'output': u"<br>".join(out_text),
            'word_list': word_list_out,
            'stats': level_stats,
            'word_sim': u"<br>".join(word_sim_out_lst)
        }
        return output


if __name__ == "__main__":
    tagger = WordLevelTagger()
    ret = tagger.tag('hw8000', u'彷彿 一切 都 沒有 了 生氣', tagger)
    print("ret=", json.dumps(ret, ensure_ascii=False).encode("UTF-8"))
    print("get_dicts=", json.dumps(tagger.get_dicts(),
          ensure_ascii=False).encode("UTF-8"))
