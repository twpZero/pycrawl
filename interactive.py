#!/usr/bin/python
# coding: utf8

from pycrawlJson import *
import code

usage_str="Try eng.printKeyWords(5) , obs.registerWord(word), obs.notify()\nOr the combo restore() ; crawl() ; obs.notify() ; save() \n"
usage_str+="To display the json : jsonDisplay.json\n"
def usage():
    print(usage_str)

code.interact(usage_str, local=locals())
