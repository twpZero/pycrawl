#!/usr/bin/python
# coding: utf8

from Engine import *

class Display:
    def __init__(self):
        pass
    def displayCategory(self,category):
        pass
    def displayUrl(self,url):
        pass
    def displaySeenUrl(self,url):
        pass
    def displayNotifiedUrl(self,url,words):
        pass
    def displaySeenNotifiedUrl(self,url,words):
        pass

class JSONDisplay(Display):
    """
    Fill an object with the data in order to dump it onto a file within the main.
    """
    def __init__(self):
        self.json={}
        self.currentCategory=""
    def displayCategory(self,category):
        if category not in self.json.keys():
            self.json[category]=[]
        self.currentCategory=category
    def displayUrl(self,url):
        self.json[self.currentCategory].append(url)
        
class ConsoleDisplay(Display):
    def __init__(self):
        pass
    def displayCategory(self,category):
        print("\n["+category+"]")
    def displayUrl(self,url):
        print("\t "+url+"")
    def displaySeenUrl(self,url):
        self.displayUrl("@old "+url)
    def displayNotifiedUrl(self,url,words):
        self.displayUrl("["+', '.join(words)+"] "+url)
    def displaySeenNotifiedUrl(self,url,words):
        self.displayUrl("@old "+"["+', '.join(words)+"] "+url)

                        
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
        self.updated=False
    def setEngine(self,engine):
        self.engine=engine
    def registerWord(self,word):
        self.register.append(word)
        self.updated=False
    def setRegister(self,register):
        self.register = register
        self.updated = False
    def _updateNotified(self):
        if self.engine != None:
            for word in self.register:
                urls=self.engine.getLinksByWord(word)
                for url in urls:
                    if url not in self.notified.keys():
                        self.notified[url]=[]
                    if word not in self.notified[url]:
                        self.notified[url].append(word)
    def notify(self):
        if not self.updated :
            self._updateNotified()
            self.updated=True
        for word in self.register:
            self.display.displayCategory(word)
            urls = self.engine.getLinksByWord(word)
            old=[] # from past days
            seens=[] # seen today
            if urls != None:
                for url in urls :
                    # si vu avant aujourd'hui
                    if url in self.seen :
                        old.append(url)
                    # si vu plusieurs fois
                    if len(self.notified[url])>1:
                        seens.append(url)
                    if url not in old and url not in seens :
                        self.display.displayUrl(url)      

            print("\t--")
            for url in seens :
                if url not in old:
                    self.display.displayNotifiedUrl(url,self.notified[url])
            print("\t--")
            for url in old :
                if url in seens :
                    self.display.displaySeenNotifiedUrl(url,self.notified[url])
                    old.remove(url)
            for url in old :
                    self.display.displaySeenUrl(url)
            del(seens)
            del(old)
