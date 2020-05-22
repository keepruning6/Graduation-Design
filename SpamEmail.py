# -*- coding:utf-8 -*-
import jieba;
import os;

class spamEmailBayes:
    #获得停用词表
    def getStopWords(self):
        stopList=[]
        for line in open("./data/DeactivateWords.txt"):
            stopList.append(line[:len(line)-1])
        return stopList;
    #获得词典
    def get_word_list(self,content,wordsList,stopList):
        #分词结果放入res_list
        res_list = list(jieba.cut(content))
        for i in res_list:
            i=i.encode('utf-8')
            if i not in stopList and i.strip()!='' and i!=None:
                if i not in wordsList:
                    wordsList.append(i)
                    
    #若列表中的词已在词典中，则加1，否则添加进去
    def addToDict(self,wordsList,wordsDict):
        for item in wordsList:
            if item in wordsDict.keys():
                wordsDict[item]+=1
            else:
                wordsDict.setdefault(item,1)
                            
    def get_File_List(self,filePath):
        filenames=os.listdir(filePath)
        return filenames
    
    #通过计算每个文件中p(s|w)来得到对分类影响最大的15个词
    #在计算过程中，若该词只出现在垃圾邮件的词典中，则令$P(w|s^{'})=0.01$，反之亦然；若都未出现，则令$P(s|w)=0.4$
    def getTestWords(self,testDict,spamDict,normDict,normFilelen,spamFilelen):
        wordProbList={}
        for word,num  in testDict.items():
            if word in spamDict.keys() and word in normDict.keys():
                #该文件中包含词个数
                pw_s=float(spamDict[word])/float(spamFilelen)                  #计算得到p(w|s)
                pw_n=float(normDict[word])/float(normFilelen)                  #计算得到p(w|n)
                ps_w=pw_s/(pw_s+pw_n)            #计算p(s|w)=p(w|s)/(p(w|s)+p(w|n))由于先验条件中出现p(s)与p(n)概率均为0.5
                wordProbList.setdefault(word,ps_w)
            if word in spamDict.keys() and word not in normDict.keys():
                pw_s=float(spamDict[word])/float(spamFilelen)
                pw_n=0.01
                ps_w=pw_s/(pw_s+pw_n) 
                wordProbList.setdefault(word,ps_w)
            if word not in spamDict.keys() and word in normDict.keys():
                pw_s=0.01
                pw_n=float(normDict[word])/float(normFilelen)
                ps_w=pw_s/(pw_s+pw_n) 
                wordProbList.setdefault(word,ps_w)
            if word not in spamDict.keys() and word not in normDict.keys():
                #若该词不在脏词词典中，概率设为0.4
                wordProbList.setdefault(word,0.4)
        sorted(wordProbList.items(),key=lambda d:d[1],reverse=True)[0:15]     #获得词频最高的15个词
        return (wordProbList)
    
    #计算贝叶斯概率
    def calBayes(self,wordList,spamdict,normdict):
        ps_w=1
        ps_n=1
         
        for word,prob in wordList.items() :
            print word+"/"+str(prob)
            ps_w*=(prob)
            ps_n*=(1-prob)
        p=ps_w/(ps_w+ps_n)
#         print(str(ps_w)+"////"+str(ps_n))
        return p        

    #计算预测结果正确率
    def calAccuracy(self,testResult):
        rightCount=0
        errorCount=0
        for name ,catagory in testResult.items():
            if (int(name)<1000 and catagory==0) or(int(name)>1000 and catagory==1):
                rightCount+=1
            else:
                errorCount+=1
        return float(rightCount)/float((rightCount+errorCount))