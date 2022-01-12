#-*- coding: utf8 -*-

import re, json
import time
from time import gmtime, strftime
import sys, os
from flask import Flask,url_for,render_template, request
from sentedit import WordLevelTagger

app = Flask(__name__, static_url_path='/sentedit2')
# debug=True 時，每當程式一修改， flask 會
# 自動重新載入 app
# app.debug = True ##啟動debug mode

# 避免重新轉址造成錯誤 
app.url_map.strict_slashes = False

@app.route('/sentedit2/<path:filename>')
def catch_all(path):
    return (f'You want path:{filename}')

@app.route("/sentedit2/")
def Index(name=None):
    return render_template('index.html',time=time.time())

wltagger=WordLevelTagger()

@app.route("/sentedit2/",methods=['GET','POST'])
def SentEdit():
    if request.method=='POST':
        output={}
        text=request.json.get('text',[])
        wordseg=request.json.get('wordseg',False)
        wordtab=request.json.get('wordtab','naer')
        corpus = request.json.get('corpus', 'MDN')
        limitWordLv = request.json.get('limitWordLv', 'inf')
        topn = int(re.sub('\D', '', request.json.get('topn', 10))) if (
            re.sub('\D', '', request.json.get('topn')) != '') else 10
        ret=wltagger.tag(wordtab, text, wordseg, corpus, limitWordLv, topn)
        output=ret
        return json.dumps(output, ensure_ascii=False).encode("UTF-8")


if __name__ == "__main__":
    # app.run(host = "0.0.0.0",port=6872)
    app.debug = True
    app.secret_key = os.urandom(16)
    app.run(port=6888)