#!/usr/bin/python
# coding: utf8

from Engine import *

class ConsoleDisplay:
    def __init__(self):
        pass
    def displayCategory(self,category):
        print("\n["+category+"]")
    def displayUrl(self,url):
        print("\t "+url+"")
    def displaySeenUrl(self,url):
        print("\t @old "+url)
    def displayNotifiedUrl(self,url,words):
        print("\t @seen ("+str(words)+") "+url)

                        
class Observer:
    def __init__(self,engine=None,display=None):
        self.engine=engine
        self.register=[]
        # seen url from past days , need json support
        self.seen=[]
        # already notified
        self.notified={}
        self.display=display
        if self.display == None:
            self.display = ConsoleDisplay()
    def setEngine(self,engine):
        self.engine=engine
    def registerWord(self,word):
        self.register.append(word)
    def _notifyWord(self,word):
        if self.engine != None:
            urls=self.engine.getLinksByWord(word)
            for url in urls:
                if url not in self.notified.keys():
                    self.notified[url]=[]
                if word not in self.notified[url]:
                    self.notified[url].append(word)
            return urls
        return None
    def notify(self):
        for word in self.register:
            self.display.displayCategory(word)
            urls = self._notifyWord(word)
            old=[]
            seens=[]
            if urls != None:
                for url in urls :
                    if len(self.notified[url])>1:
                        seens.append(url)
                    else :
                        if url in self.seen :
                            old.append(url)
                        else :
                            self.display.displayUrl(url)      

            for url in seens :
                self.display.displayNotifiedUrl(url,self.notified[url])
            for url in old :
                self.display.displaySeenUrl(url)
            del(seens)
            del(old)
