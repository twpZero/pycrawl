#!/usr/bin/python
# coding: utf8

"""
@author twpDone / twp_zero
@file pycrawl.py
Parser pour la veille, il parcours les pages et collecte les associations keyword/lien url.
Le but et de pouvoir afficher les articles pour un mot clé, et d'eviter de lire 20 fois des contenus similaires.

"""

# import des modules de parsage d'arguments, de fichiers de configuration 
# et la lib url pour le parcours des liens
import argparse, configparser, urllib.request
# Classe de parsage
from html.parser import HTMLParser
# Methode pour créer des liens absolus.
from urllib.parse import urljoin
import re
import json

# Nom par defaut du fichier de conf
CONFIG_FILE="crawl.conf"

def genConfigFile(cp):
    """
    @function genConfigFile
    Genere le fichier de configuration par defaut
    @param cp Objet configparser.
    """
    global CONFIG_FILE
    
    # Liste des sources
    cp.add_section("Seeds")
    cp.set("Seeds","sourcesList","http://www.securityweek.com/cybercrime, https://threatpost.com/")
    
    # Gestion des mots en liste noire
    cp.add_section("Words")
    cp.set("Words","wordBlacklist","all,to,on,cyber,led,more,can,threatpost,how,lab,data,a,not,featured,story,management,that,and,are,be,news,is,it,in,make,the,latest,for,of,or,off,with,us,you,read,security,wrap,cow,as,under,did,list,item,what,tags,let,forum,use,names,so,nor,suits,learn,didnt,write,le,foo,might,day,re,days,uses,one,their,any,also,take,see,article,been,an,say,look,if,via,know,known,some,election,sight,step,run,from,for,your,there,don,but,year,years,tip,at,why,vow,using,by")
    
    # ouverture et écriture du ficher de conf
    f=open(CONFIG_FILE,"w")
    cp.write(f)
    f.close()

def readConfigFile(cp):
    """
    @function readConfigFile
    Lit le fichier de configuration par defaut
    @param cp Objet configparser.
    """
    global CONFIG_FILE
    cp.read(CONFIG_FILE)

def getConfigWordsBlackList(cp):
    """
    @function getConfigWordsBlackList
    Recupere dans le fichier de config la list des mots blacklistés
    @param cp Objet configparser.
    @return List unicode wordBlackList
    @raise Exception  Erreur de lecture du fichier
    """
    if cp.has_section("Words"):
        try : 
            return cp.get("Words","wordBlacklist").split(",")
        except Exception as ex:
            raise ex

def getConfigSourcesList(cp):
    """
    @function getConfigSourcesList
    Recupere dans le fichier de config la list des sites a parser
    @param cp Objet configparser.
    @return List unicode sourcesList
    @raise Exception  Erreur de lecture du fichier
    """
    if cp.has_section("Seeds"):
        try : 
            return cp.get("Seeds","sourcesList").split(",")
        except Exception as ex:
            raise ex

from NewsParser import *
from Engine import *
from Observer import *
import json

def jsonDump(self):
    return self.__dict__

def save():
    global eng
    global obs
    f=open("register.dump","w")
    json.dump(obs.register,f)
    f.close()
    f=open("links.dump","w")
    json.dump(eng.links,f)
    f.close()

def restore():
    global eng
    global obs
    try :
        f=open("register.dump","r")
        obs.setRegister(json.load(f))
        f.close()
    except:
        pass
    try :
        f=open("links.dump","r")
        links=json.load(f)
        obs.seen = links.keys()
        eng.links = links
        f.close()
    except:
        pass

def crawl():
    global np
    np.crawl()
### MAIN ###

cp=configparser.ConfigParser()
#genConfigFile(cp)
readConfigFile(cp)

seedsList=getConfigSourcesList(cp)
blackList=getConfigWordsBlackList(cp)

eng=Engine()
eng.setWordBlackList(blackList)

np=NewsParser(seedsList, engine=eng)
jsonDisplay=JSONDisplay()
obs = Observer(eng,jsonDisplay)


if __name__=="__main__":
    restore()
    crawl()
    obs.notify()
    save()
    
    jsonToDump={}
    jsonToDump["Veille"]=jsonDisplay.json
    jsonToDump["Trends"]={}
    for count in eng.getWordsCounts() :
        if count >= 5:
            jsonToDump["Trends"][count]=",".join(eng.getWordsByCount(count))
    f=open("pycrawlfeed.json","w")
    json.dump(jsonToDump,f)
    f.close()

    #eng.listWords()
    print("\n")
