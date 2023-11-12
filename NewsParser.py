#!/usr/bin/python
# coding: utf8

# import des modules de parsage d'arguments, de fichiers de configuration 
# et la lib url pour le parcours des liens
import argparse, configparser, urllib.request
# Classe de parsage
from html.parser import HTMLParser
# Methode pour créer des liens absolus.
from urllib.parse import urljoin
import re

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
        self.opener = urllib.request.build_opener()
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
                    htmldata=response.read()
                    try :
                        # Encodage obligatoire des données
                        htmldata=htmldata.decode('utf8', errors='replace')
                        # -> Natively handled in python3 ?
                    except Exception as ex1:
                        raise ex1
                    # fermeture de la socket en cas de reussite
                    response.close()
                    # debut du parsing
                    self.feed(htmldata)
                except urllib.request.HTTPError as herror:
                    # Gestion de la fermeture de la socket en cas d'erreur
                    if response != None:
                        response.close()
                    raise herror
                except Exception as ex:
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
            except urllib.request.HTTPError as httperr:
                print("[-] HTTPError "+str(httperr)+">"+str(httperr.reason))
            except Exception as ex:
                print("[-] Crawling Exception "+str(ex))

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

