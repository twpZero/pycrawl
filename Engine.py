#!/usr/bin/python
# coding: utf8

# import des modules de parsage d'arguments, de fichiers de configuration 
# et la lib url pour le parcours des liens
import argparse, ConfigParser, urllib2
# Classe de parsage
from HTMLParser import HTMLParser
# Methode pour créer des liens absolus.
from urlparse import urljoin
import re


class Engine:
    """
    @class Engine
    Moteur de correlation pour liens et pages parcourus.

    @attr words Mot vus, dict{Mot:Count}
    @attr links Liens vus, dict{url,[mots,clés]}
    @attr wordBlacklist List de mots à ne pas traiter
    @attr linksBlacklist List de liens à ne pas traiter
    @attr sortedWords Table d'association des mots avec leur nombre d'occurence

    """
    def __init__(self):
        """
        @method init

        """
        self.words={}
        self.links={}
        self.wordBlacklist=[]
        self.linksBlacklist=[]
        self.sortedWords={}

    def setWordBlackList(self,wbl):
        """
        @method setWordBlackList
        @param wbl List of blacklisted words
        """
        self.wordBlacklist=wbl

    def _processWord(self,word):
        """
        @method _processWord
        Sanitise the inputs and return it
        @param word str/unicode
        @return unicode word
        """
        w=word
        if re.search("^http",w)!=None:
            w="" 
        if type(word) !=unicode:
            w=w.decode("utf8")
        w=w.replace(u"[","")
        w=w.replace(u"]","")
        w=w.replace(u".","")
        w=w.replace(u":","")
        w=w.replace(u",","")
        w=w.replace(u"(","")
        w=w.replace(u")","")
        w=w.replace(u"\t","")
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
        """
        @method _addWord
        Add word in the word counter
        @Note Handle the blacklist feature
        @param word unicode word to add
        """
        if len(word) > 1 :
            if word not in self.wordBlacklist :
                if word not in self.words.keys():
                    self.words[word]=1
                else:
                    self.words[word]+=1
    
    def addLink(self,href,strWordList):
        """
        @method addLink
        Add link with the corresponding keywords in the engine
        @param href unicode url 
        @param strWordList List unicode of related keywords
        @note Hande blacklist feature
        """
        if href not in self.links.keys():
            # gestion du cas ou l'index -1 n'existe pas
            if len(href)>0:
                # Ajout de / à la fin si necessaire
                if href[-1] != "/" :
                    href=href+"/"
            # Initialisation des la liste de mots clés, si le lien n'este pas deja
            self.links[href]=[]
        # recuperer chaque mot
        for word in strWordList.split(" "):
            # sanitise input
            word=self._processWord(word)
            if len(word) > 1:
                if word not in self.wordBlacklist :
                    # ajout du mot clé à la liste
                    self.links[href].append(word.lower())
                    # comptage du mot clé
                    self._addWord(word.lower())

    def top(self,numberOfMatch):
        """
        @method top
        Return words and related links if they match more than *numberOfMatch* times
        @print words, count and related link
        @note To be printed you may use str instead of unicode strings
        """
        for word,count in self.words.iteritems():
            if count >= numberOfMatch:
                sentence="\n"+word+" ("+str(count)+")"
                if type(sentence)!=unicode:
                    sentence=sentence.decode('utf8', errors='replace')
                print(sentence.encode("utf8",errors="replace"))
                for href,tab in self.links.iteritems():
                    if word in tab :
                        print("\t"+href.encode("utf8",errors="replace"))

    def _sort(self):
        if len(self.sortedWords) == 0:
            for word,count in self.words.iteritems():
                if count not in self.sortedWords.keys():
                    self.sortedWords[count]=[]
                self.sortedWords[count].append(word)
    
    def getWordsCounts(self):
        self._sort()
        return self.sortedWords.keys()
    
    def getMaxWordCount(self):
        return max(self.getWordsCounts())
        
    def listWords(self):
        self._sort()
        for count,words in self.sortedWords.iteritems():
            l=""
            for word in words:
                l+= word+" , "
            print(str(count)+" "+l)

    def getWordsByCount(self,count):
        self._sort()
        try : 
            return self.sortedWords[count]
        except:
            return []
                
    def getLinksByWord(self,word):
        hrefs=[]
        for href,tab in self.links.iteritems():
            if word in tab :
                hrefs.append(href)
        return hrefs
    
    def printKeyWords(self,maxCount):
        for count in self.getWordsCounts() :
            if count >= maxCount:
                print(str(count)+" "+str(self.getWordsByCount(count)))

