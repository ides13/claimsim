# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 05:17:53 2020

@author: ides1
"""

from typing import NamedTuple
import re
import requests

#===============================================================================
# 從專利號碼、公開號等取得下載的網址 UrlToken 。
#===============================================================================
class UrlToken(NamedTuple):
    type: str
    value: str
    digital:str
    url:str
    #allgrou:str

def tokenize(patentno):
    #keywords = {'PN', 'PGNR'}
    token_specification = [
        ('PN',       r'US(?P<PN_Dig>\d{7})[AB][1-3]?'),          # Patent Number      : _groups[1]
        ('PGNR',     r'US(?P<PGNR_Dig>\d{11})[A][1-3]?'),           # Publication Number : _groups[3]
        ('MISMATCH', r'.*'),                          # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    #print(tok_regex)   
    mo = re.match(tok_regex, patentno)
    if mo:
        kind = mo.lastgroup
        #_groups = mo.groups()
        value = mo.group()

        if kind == 'PN':
            digital = mo.group('PN_Dig') # _groups[1]
            url = '''http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1&Sect2=HITOFF&p=1&u=/netahtml/PTO/srchnum.html&r=1&f=G&l=50&d=PALL&s1={no}.PN.
                    '''.strip().format(no=digital)
        elif kind == 'PGNR':
            digital = mo.group('PGNR_Dig') # _groups[3]
            url = '''http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1&Sect2=HITOFF&p=1&u=/netahtml/PTO/srchnum.html&r=1&f=G&l=50&d=PG01&s1={no}.PGNR.
                    '''.strip().format(no=digital)
        elif kind == 'MISMATCH':
            #raise RuntimeError(f'{value!r} unexpected on Type')            
            #print(patentno + "非合法號碼")
            value =  '{}(非合法號碼)'.format(value)
            digital = '非法號碼無法匹配'
            url = '{}(非合法號碼)'.format(mo.group('MISMATCH'))
    return UrlToken(kind, value, digital, url)
    #return UrlToken(kind, value, url, digital, _groups)S

#===============================================================================
# 下載專利網頁，以及分析網頁內容，取得專利的書目資料、說明書資料等。
#===============================================================================
#下載網頁
def download_patent_html(patentno:str):
    geted_url = tokenize(patentno).url
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    response = requests.get(geted_url, headers = {'user-agent': user_agent})                                    #(url, allow_redirects=True) 
    open(patentno+".html", 'wb').write(response.content)            #, encoding='UTF-8'
    
    fp = open("urldownload.txt", "a")
    fp.write('\n{}'.format(geted_url))
    fp.close()
    return
    #fp.close()return


#===============================================================================
# 分析網頁內容，取得專利的書目資料、說明書資料等。
#===============================================================================
import DanEadsPypatent as pypatent

def thispatent(num:str):
    # Create a Patent object
    this_patent = pypatent.Patent(title='Null',
                                    url= tokenize(num).url)
    this_patent.fetch_details()    # Fetch the details 
    # 所得到的 claims 中，claims[0]有時不是請求項1，因此要去除。
    if 'What is claimed is' in this_patent.claims[0]:
        this_patent.claims.pop(0)
    return this_patent


#===============================================================================
# 計算兩個句子的相似度
#===============================================================================
import numpy as np
from scipy import spatial
import gensim
#import pyemd

#load word2vec model, here GoogleNews is used
vecfile = "D:\OpenData\GoogleNews-vectors-negative300.bin"
model = gensim.models.KeyedVectors.load_word2vec_format(vecfile, binary=True)
#two sample sentences 
index2word_set = set(model.wv.index2word)

#第一種算法：如果使用word2vec，需要計算每個句子/文檔中所有單詞的平均向量，並使用向量之間的餘弦相似度來計算句子相似度。
def avg_feature_vector(sentence, model, num_features, index2word_set):
    words = sentence.split()
    feature_vec = np.zeros((num_features, ), dtype='float32')
    n_words = 0
    for word in words:
        if word in index2word_set:
            n_words += 1
            feature_vec = np.add(feature_vec, model[word])
    if (n_words > 0):
        feature_vec = np.divide(feature_vec, n_words)
    return feature_vec

def calsim(sentance1, sentance2):
    try:
        s1_afv = avg_feature_vector(sentance1, model=model, num_features=300, index2word_set=index2word_set)
        s2_afv = avg_feature_vector(sentance2, model=model, num_features=300, index2word_set=index2word_set)
        sim = 1 - spatial.distance.cosine(s1_afv, s2_afv)
    except:
        sim = 0
    return sim


#===============================================================================
#主程式。
#===============================================================================


if __name__ == '__main__':   
    #pass

    #sentance1 指的是一個技術的描述，最簡單的方法就是一個發明的請求項的記載方式
    sentance1 = "A battery system comprising: a group of three or more battery cells; and a connector electrically connecting the group of three of more battery cells together in parallel, the cell connector comprising a unitary conductor having at least one fuse integrally formed therein such that at least one fuse is located electrically between a first battery cell and a plurality of other battery cells in the group of three or more battery cells."
    
    #patentlist 提供想要比對的美國專利書號碼，例如['US7654301B2', 'US7654300B2', 'US7654329B2']
    patentlist = ['US6608470B1', 'US6924620B2', 'US8795865B2', 'US8932741B2', 'US9136512B2', 'US9263878B2', 'US9318734B2']
    
    fp = open("claim_similarity.txt", "a")    
    for i in patentlist:
        p = thispatent(i)
        
        sentance2 = p.claims[0]
        sim = calsim(sentance1, sentance2)
        print(   '  與%s的請求項1間的相似度 = %s' % (i, sim))
        fp.write('\n與%s的請求項1間的相似度 = %s' % (i, sim))
        
        for index, paragraph in enumerate(p.description, start =3):
            sentance2 = paragraph
            sim = calsim(sentance1, sentance2)
            print(   '  與%s的段落%s間的相似度 = %s' % (i, index, sim))
            fp.write('\n與%s的段落%s間的相似度 = %s' % (i, index, sim))
        #end for paragraph in p.description[3:]
    #end for i in patentlist:
    fp.close()
