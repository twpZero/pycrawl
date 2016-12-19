#!/usr/bin/python
# coding: utf8

from pycrawl import *
import code

usage_str="Try eng.listWords() , obs.registerWord(word), obs.notify()\nOr the combo restore() ; crawl() ; obs.notify() ; save() \n"
def usage():
    print(usage_str)

code.interact(usage_str, local=locals())
