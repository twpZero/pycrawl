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
import argparse, ConfigParser, urllib2
# Classe de parsage
from HTMLParser import HTMLParser
# Methode pour créer des liens absolus.
from urlparse import urljoin

# Nom par defaut du fichier de conf
CONFIG_FILE="crawl.conf"

def genConfigFile(cp):
    """
    @function genConfigFile
    Genere le fichier de configuration par defaut
    @param cp Objet ConfigParser 
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
    @param cp Objet ConfigParser 
    """
    global CONFIG_FILE
    cp.read(CONFIG_FILE)

def getConfigWordsBlackList(cp):
    """
    @function getConfigWordsBlackList
    Recupere dans le fichier de config la list des mots blacklistés
    @param cp Objet ConfigParser 
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
    @param cp Objet ConfigParser 
    @raise Exception  Erreur de lecture du fichier
    """
    if cp.has_section("Seeds"):
        try : 
            return cp.get("Seeds","sourcesList").split(",")
        except Exception as ex:
            raise ex

class NewsParser(HTMLParser):
    """
    @class NewsParser
    Effectue les requettes http et le parsage des pages en HTML, 
    Realise le "stockage" dans le moteur de correlation si fourni.
    Gere les sources multiples, et liens déjà visités.
    @note le user-agent est hard-codé

    @attr seeds List de pages a visiter
    @attr engine Moteur de corellation à utiliser
    @attr browsed List de pages deja visitées
    @attr currentSeed Page actuellement parsée
    @attr currentTag Type de balise actuellement parsée
    @attr currentHref Lien actuellement parsé
    @attr currentData Données de la balise actuellement parsée.
    @attr opener 'Navigateur' à utiliser pour parcourir les pages.
    """
    def __init__(self,seeds=[],engine=None):
        """
            @method init
            @param seeds Str List des pages à parser
            @param engine Objet Engine pour le classage des liens.
        """
        HTMLParser.__init__(self)
        self.seeds = seeds
        self.engine = engine
        self.browsed = []
        self.currentSeed = ""
        self.currentTag = ""
        self.currentHref = ""
        self.currentData = ""
        self.opener = urllib2.build_opener()
        # Set User agent
        self.opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

    def nextSeed(self):
        """
        @method nextSeed
        Pacours la page suivante, gere les pages deja visitées.
        @raise Exception en case d'erreur de lecture de la page ou d'erreur socket
        """
        self.browsed.append(self.currentSeed)
        # si il reste des pages a parcourir
        if len(self.seeds) > 0:
            # depile le dernier element
            self.currentSeed = self.seeds.pop()
            if self.currentSeed not in self.browsed:
                response = None
                try :
                    print("[+] Crawling :"+self.currentSeed)
                    # Ouverture de l'url
                    response = self.opener.open(self.currentSeed)
                    # Encodage obligatoire des données
                    self.feed(response.read().decode('utf-8'))
                    # fermeture de la socket en cas de reussite
                    response.close()
                except Exception as ex:
                    # Gestion de la fermeture de la socket en cas d'erreur
                    if response != None:
                        response.close()
                    raise ex
        else :
            self.currentSeed = ""

    def crawl(self):
        """
        @method crawl
        Parcours les pages une par une tant que la liste n'est pas vide
        @note attention la methode nextSeed doit faire un pop de la liste sinon on boucle à l'infini
        @raise Exception en case d'erreur de lecture de la page ou d'erreur socket
        """
        while len(self.seeds) > 0:
            try:
                self.nextSeed()
            except Exception as ex:
                print("[-] "+str(ex)+">"+ex.message)

    def handle_starttag(self,tag,attrs):
        """
        @override HTMLParser
        @method handle_starttag
        Gere la lecture d'un nouveau tag html
        @param tag La balise lue
        @param attrs Attributs html de la balise
        @note les liens sont a recuperer dans les attributs (href)
        """
        self.currentTag = tag
        # gestion des balises de lien/anchor (<a href="....">lien</a>)
        if self.currentTag == "a":
            for attrib in attrs:
                # recuperation de l'attribut href
                if attrib[0] == "href":
                    # generation d'un lien absolu
                    self.currentHref = urljoin(self.currentSeed+"/",attrib[1])
        else :
            self.currentHref = ""
    
    def handle_endtag(self, tag):
        """
        @override HTMLParser
        @method handle_starttag
        Gere la fin de lecture d'un tag html, methode de nettoyage des valeurs.
        @param tag La balise lue
        """
        self.currentTag = ""
        self.currentHref = ""
        self.currentData = ""

    def  handle_data(self, data):
        """
        @override HTMLParser
        @method handle_starttag
        Gere la lecture des données contenues dans le tag html (entre les balises)
        @param data Les données texte situées entre les balises
        """
        if self.currentTag != "":
            self.currentData = data
            # recuperation des liens et balises de titre
            if self.currentTag in ["a","h1","h2"]:
                # Gestion de l'url pour les balises titre = utilisation de l'url en cours de parcours.
                # @note peut être pas aussi genial que prévu car certains sites mettent des titres pour présenter les liens ...
                if self.currentTag in ["h1","h2"]:
                    self.currentHref=self.currentSeed
                if self.engine == None:
                    # affichage en mode console (nul)
                    print(self.currentTag+" ["+self.currentHref+"]"+self.currentData.replace("\n"," "))
                else :
                    # Avec moteur de correlation
                    self.engine.addLink(self.currentHref,self.currentData.replace("\n"," "))
        self.currentData = ""

class Engine:
    """
    @class Engine
    Moteur de correlation pour liens et pages parcourus.

    @attr words Mot vus, dict{Mot:Count}
    @attr links Liens vus, dict{url,[mots,clés]}
    @attr wordBlacklist List de mots à ne pas traiter
    @attr linksBlacklist Listde liens à ne pas traiter

    """
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
