# claimsim

1、建議安裝，anaconda python。

2、gensim 套件。

3、找出「一個技術描述(sentance1)」，與 「patentlist 中各專利請求項1 」間的相似度，使用方式如下：
#sentance1 指的是一個技術的描述，最簡單的方法就是一個發明的請求項的記載方式
#patentlist 提供想要比對的美國專利書號碼，例如['US7654301B2', 'US7654300B2', 'US7654329B2']
4、改變3中的變數執行後，會得到claim_similarity.txt的文件，打開該文件後，可以得到相似度的計算值。
5、結果。
如果把一件專利的不同組的請求項，當作sentance1時，相似度會達0.9以上。因此，這樣的方法有實用上的「可能性」，但還需要優化。
