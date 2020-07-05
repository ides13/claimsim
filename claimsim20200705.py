#===============================================================================
# 爬Google美國的美專說明書
#===============================================================================

from bs4 import BeautifulSoup
import requests
  
def download_patent_html (patentno):
    url = 'https://patents.google.com/patent/{}'.format(patentno)   
    response = requests.get(url)                                    #(url, allow_redirects=True) 
    open(patentno+".html", 'wb').write(response.content)            #, encoding='UTF-8'
    
    fp = open("urldownload.txt", "a")
    fp.write('\n{}'.format(url))
    fp.close()
    return


class Patent:
    def __init__(self, no_patent=""):
        self.fetched_details = False
        self.claim01 = None
        self.abstract = None 
        self.data = None      
        self.patent_num = no_patent
  
        try:
            self.fetch_details()
        except FileNotFoundError:
            print("No such file or directory:" + self.patent_num + ".html")
            download_patent_html (self.patent_num)
            print("downloaded")        
            self.fetch_details()
        return

    def fetch_details(self):
        self.fetched_details = True
        self.data = open(self.patent_num + ".html", 'rb').read()
        
        soup = BeautifulSoup(self.data, 'html.parser')
        try:
            self.patent_date = 1
        except:
            pass

        try:
            # Get abstract # 
            abstractsoup = soup.find('meta',attrs={'name':'DC.description'})
            self.abstract = abstractsoup['content']  # Get text         
        except:
            pass

        try:
            claim01soup = soup.find('div', num='00001')
            self.claim01 = claim01soup.text  # Get text 
        except:
            pass
        return
    
    #[class Patent]
    def as_dict(self) -> dict:
        """
        Return patent info as a dict
        :return: dict
        """
        if self.fetched_details:
            d = {
                 'abstract': self.abstract,
                'claim01': self.claim01,
            }
        else:
            print("error")
        return d
    #[class Patent]
    def __repr__(self):
        return str(self.as_dict())

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
    sentance1 = "A battery system" 
    
    #patentlist 提供想要比對的美國專利書號碼，例如['US7654301B2', 'US7654300B2', 'US7654329B2']
    patentlist = ['US7654301B2', 'US7654300B2', 'US7654329B2']
    
    for i in patentlist:
        p = Patent(i)
        sentance2 = p.claim01
        sim = calsim(sentance1, sentance2)
        print('與%s間的相似度 = %s' % (i, sim))
        fp = open("claim_similarity.txt", "a")
        fp.write('\n與%s間的相似度 = %s' % (i, sim))
        fp.close()
    #end for
