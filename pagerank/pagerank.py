import numpy as np
import xlrd 
import xlwt 
import heapq


class PageRank:
    def __init__(self,pages=['A','B'],links=[(1,0),(0,1)],d=0.85):
        self.pages = pages;
        self.links = links;
        self.dtype = np.float64; 
        self.d = d; 
        self.pageRanks = np.array([ 1/(len(self.pages)) ]*len(self.pages)); # np.ones(len(self.pages), dtype = self.dtype); # 初始化每个页面PR值：1 or 1 / N or other 【利用numpy数组化，方便进行算术运算，原生python列表不支持此类运算】经过几组数据测试，此初始值确实不会影响最终的PR收敛值
        self.inputLinksList = [[]]*len(self.pages); 
        for i in range(len(self.inputLinksList)):
            self.inputLinksList[i]=[];
            pass;
        # print("in:\n",self.inputLinksList)
        for item in self.links: # (n,m)：n指向m
        #     print(i)
            self.inputLinksList[item[1]].append(item[0]);
            pass;
        self.outputLinksList = [[]]*len(pages); 
        for item in range(len(self.outputLinksList)):
            self.outputLinksList[item]=[];
            pass;
        # print("out:\n",self.outputLinksList)
        for item in self.links: 
        #     print(i)
            self.outputLinksList[item[0]].append(item[1]);
            pass;
        
    def getInputLinksList(self):
        # print("in:\n",self.inputLinksList)
        return self.inputLinksList;

    def getOutputLinksList(self):
        # print("out:\n",self.getOutputLinksList)
        return self.outputLinksList;
    
    def getCurrentPageRanks():
        return self.pageRanks;
    
    def getLinks():
        return self.links;

    def iterOnce(pageRanks,d,links,inputLinksList,outputLinksList): 
        pageRanks = np.copy(pageRanks); 
        # print("input pageRanks:",pageRanks);
        # print("input d:",d);
        for i in range(0,len(pageRanks)):
            result = 0.0;
            for j in inputLinksList[i]: # inputLinksList[i]：第i个节点的(入度)节点[下标]列表
                # print (inputLinksList[i]);
                result += pageRanks[j]/len(outputLinksList[j]);
                # print("[",j,"] pageRanks[j]:",pageRanks[j]," len(outputLinksList[j]:",len(outputLinksList[j]));
                pass;
            # print("[",i,"] result:",result);
            pageRanks[i] = (1 - d) + d*result;
            # print("[",i,"] pr:",pageRanks[i]);
            pass;
        return pageRanks;
    
    def maxAbs(array): 
        max = 0; 
        for i in range(0,len(array)):
            if abs(array[max]) < abs(array[i]):
                max = i;
                pass;
            pass;
        return max; 
    
    def train(self,maxIterationSize=100,threshold=0.0000001): 
        print("[PageRank.train]",0," self.pageRanks:",self.pageRanks);
        iteration=1;
        lastPageRanks = self.pageRanks; 
        difPageRanks = np.array([100000.0]*len(self.pageRanks),dtype=self.dtype); 
        while iteration <= maxIterationSize:
            if ( abs(difPageRanks[PageRank.maxAbs(difPageRanks)]) < threshold ):
                break;
            self.pageRanks = PageRank.iterOnce(lastPageRanks,self.d,self.links,self.inputLinksList,self.outputLinksList);
            difPageRanks = lastPageRanks - self.pageRanks ; # self.pageRanks在初始化__init__中已通过numpy向量化
            # print("[PageRank.train]",iteration," lastPageRanks:",lastPageRanks);
            print("[PageRank.train]",iteration," self.pageRanks:",self.pageRanks);
            # print("[PageRank.train]",iteration," difPageRanks:",difPageRanks);
            lastPageRanks = np.array(self.pageRanks);
            iteration += 1;
            pass;
        print("[PageRank.train] iteration:",iteration-1);#test
        # print("[PageRank.train] difPageRanks:",difPageRanks) # test
        return self.pageRanks;

    pass; # end class


def topN(a,num=5):
    # return the indexes of top N biggest numbers in a array
    # a is the array, num is N
    return list(map(a.index,heapq.nlargest(num,a)))
    # pass
edge_dir = './edge.xlsx'
node_dir = './node.xlsx'

workbook = xlrd.open_workbook(node_dir)
sheet = workbook.sheet_by_index(0)
pages = sheet.col_values(0)
# print(pages)
pages.pop(0)
# print(pages)

workbook = xlrd.open_workbook(edge_dir)
sheet = workbook.sheet_by_index(0)
sources = sheet.col_values(0)
sources.pop(0)
targets = sheet.col_values(1)
targets.pop(0)
links = [] 
for i in range(len(sources)):
    links.append((int(sources[i]),int(targets[i]))) # find the top brand
    # links.append((int(targets[i]),int(sources[i]))) # find the top designer

d = 0.9

pageRank = PageRank(pages,links,d);
pageRanks = pageRank.train(12,0.000000000001); # pageRanks:各节点的PR值
print("pageRanks:",pageRanks);
print("sum(pageRanks) :",np.sum(pageRanks));

print("getInputLinksList:",pageRank.getInputLinksList());
print("getOutputLinksList:",pageRank.getOutputLinksList());

# print (pageRanks.shape)
pageRanks = pageRanks.tolist()
# pageRanks [] = pageRanks.getA()
# print(type(pageRanks))
# print(pageRanks)
top_num = 20
top_index = topN(pageRanks,top_num)
for i in range(int(top_num/2)):
    print('%-18s:%-5.5s\t %-13s:%-5.5s'%(pages[top_index[2*i]],pageRanks[top_index[2*i]],pages[top_index[2*i+1]],pageRanks[top_index[2*i+1]]))
