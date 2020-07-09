# claimsim
claimsim_20200705.py

1、建議安裝，anaconda python。並且，需要gensim 套件。

2、功能：找出「一個技術描述(sentance1)」，與 「patentlist 中各專利請求項1 」間的相似度。

3、此程式的使用方式如下：

#sentance1 指的是一個技術的描述，最簡單的方法就是一個發明的請求項的記載方式。

#patentlist 提供想要比對的美國專利書號碼，例如['US7654301B2', 'US7654300B2', 'US7654329B2']。

4、改變3中的變數執行後，會得到claim_similarity.txt的文件，打開該文件後，可以得到相似度的計算值。

5、結果：如果把一件專利的不同組的請求項，當作sentance1時，相似度會達0.9以上。因此，這樣的方法有實用上的「可能性」，但還需要優化。

claimsim_20200708.py

1、需要pypatent的檔案，我要修正它，所以直接下載並修正檔名為「DanEadsPypatent」來使用，請同時下載該檔案。

2、本案是爬美國專利資料庫，已可以爬公開說明書和專利說明書。

3、本次修正，已可以計算整個說明書的段落的近似值，只是段落的編號與說明書編號不一樣。請用p = thispatent('US6924620B2').description[3]來查詢段落內容。

4、與前次版本不同，本次不會下載任何檔案，是以後修正的目標。

