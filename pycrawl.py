#!/usr/bin/python
# coding: utf8

import argparse, ConfigParser, urllib2
from HTMLParser import HTMLParser
from urlparse import urljoin


def genConfigFile(cp):
    global CONFIG_FILE
    cp.add_section("Seeds")
    cp.set("Seeds","sourcesList","http://www.securityweek.com/cybercrime, https://threatpost.com/")
    cp.add_section("Words")
    cp.set("Words","wordBlacklist","all,to,on,cyber,led,more,can,threatpost,how,lab,data,a,not,featured,story,management,that,and,are,be,news,is,it,in,make,the,latest,for,of,or,off,with,us,you,read,security,wrap,cow,as,under,did,list,item,what,tags,let,forum,use,names,so,nor,suits,learn,didnt,write,le,foo,might,day,re,days,uses,one,their,any,also,take,see,article,been,an,say,look,if,via,know,known,some,election,sight,step,run,from,for,your,there,don,but,year,years,tip,at,why,vow,using,by")
    f=open(CONFIG_FILE,"w")
    cp.write(f)
    f.close()

def readConfigFile(cp):
    global CONFIG_FILE
    cp.read(CONFIG_FILE)

def getConfigWordsBlackList(cp):
    if cp.has_section("Words"):
        try : 
            return cp.get("Words","wordBlacklist").split(",")
        except Exception as ex:
            raise ex

def getConfigSourcesList(cp):
    if cp.has_section("Seeds"):
        try : 
            return cp.get("Seeds","sourcesList").split(",")
        except Exception as ex:
            raise ex

class NewsParser(HTMLParser):
    def __init__(self,seeds=[],engine=None):
        HTMLParser.__init__(self)
        self.seeds = seeds
        self.engine = engine
        self.browsed = []
        self.currentSeed = ""
        self.currentTag = ""
        self.currentHref = ""
        self.currentData = ""
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

    def nextSeed(self):
        self.browsed.append(self.currentSeed)
        if len(self.seeds) > 0:
            self.currentSeed = self.seeds.pop()
            if self.currentSeed not in self.browsed:
                response = None
                try :
                    print("[+] Crawling :"+self.currentSeed)
                    response = self.opener.open(self.currentSeed)
                    self.feed(response.read().decode('utf-8'))
                    response.close()
                except Exception as ex:
                    if response != None:
                        response.close()
                    raise ex
        else :
            self.currentSeed = ""

    def crawl(self):
        while len(self.seeds) > 0:
            try:
                self.nextSeed()
            except Exception as ex:
                print("[-] "+str(ex)+">"+ex.message)

    def handle_starttag(self,tag,attrs):
        self.currentTag = tag
        if self.currentTag == "a":
            for attrib in attrs:
                if attrib[0] == "href":
                    self.currentHref = urljoin(self.currentSeed+"/",attrib[1])
        else :
            self.currentHref = ""
    
    def handle_endtag(self, tag):
        self.currentTag = ""
        self.currentHref = ""
        self.currentData = ""

    def  handle_data(self, data):
        if self.currentTag != "":
            self.currentData = data
            if self.currentTag in ["a","h1","h2"]:
                if self.currentTag in ["h1","h2"]:
                    self.currentHref=self.currentSeed
                if self.engine == None:
                    print(self.currentTag+" ["+self.currentHref+"]"+self.currentData.replace("\n"," "))
                else :
                    self.engine.addLink(self.currentHref,self.currentData.replace("\n"," "))
        self.currentData = ""
        pass

class Engine:
    def __init__(self):
        self.words={}
        self.links={}
        self.wordBlacklist=[]
        self.linksBlacklist=[]

    def setWordBlackList(self,wbl):
        self.wordBlacklist=wbl

    def _processWord(self,word):
        w=word.encode("utf8").decode("utf8")
        w=w.replace(u"[","")
        w=w.replace(u"]","")
        w=w.replace(u".","")
        w=w.replace(u":","")
        w=w.replace(u",","")
        w=w.replace(u"(","")
        w=w.replace(u")","")
        w=w.replace(u" ","")
        w=w.replace(u'"','')
        w=w.replace(u"’","")
        w=w.replace(u"‘","")
        w=w.replace(u"'","")
        w=w.replace(u"`","")
        w=w.replace(u"…","")
        w=w.lower()
        return w
    def _addWord(self,word):
        if len(word) > 1 :
            if word not in self.wordBlacklist :
                if word not in self.words.keys():
                    self.words[word]=1
                else:
                    self.words[word]+=1
    
    def addLink(self,href,strWordList):
        if href not in self.links.keys():
            if href[-1] != "/" :
                href=href+"/"
            self.links[href]=[]
        for word in strWordList.split(" "):
            word=self._processWord(word)
            if word not in self.wordBlacklist :
                self.links[href].append(word.lower())
                self._addWord(word.lower())
    def top(self,numberOfMatch):
        for word,count in self.words.iteritems():
            if count >= numberOfMatch:
                sentence="\n"+word+" ("+str(count)+")"
                print(sentence.encode("utf8"))
                for href,tab in self.links.iteritems():
                    if word in tab :
                        print("\t"+href)
                

CONFIG_FILE="crawl.conf"
cp=ConfigParser.ConfigParser()
genConfigFile(cp)
readConfigFile(cp)

seedsList=getConfigSourcesList(cp)
blackList=getConfigWordsBlackList(cp)

eng=Engine()
eng.setWordBlackList(blackList)

np=NewsParser(seedsList, engine=eng)
np.crawl()

eng.top(5)

# TODO sort by count
