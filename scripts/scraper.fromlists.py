#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import codecs

from bs4 import BeautifulSoup

from wekeypedia import WikipediaPage as page

# lists = [
#   u"List_of_philosophers_(A–C)",
#   u"List_of_philosophers_(D–H)",
#   u"List_of_philosophers_(I–Q)",
#   u"List_of_philosophers_(R–Z)",
#   u"List_of_Chinese_philosophers"
# ]

lists = codecs.open("../datasets/seeds.txt", "r", "utf-8").read().split("\n")

def get_html(name):
  p = page(name, "en")
  content = p.get_current()

  return content

def extract_list(html):
  soup = BeautifulSoup(html, "html.parser")

  result = []

  if len(soup.select("h2 + ul")) > 0:
    li = reduce(lambda a,b: a+b, [ ul.find_all("li") for ul in soup.select("h2 + ul") ])

    li = [ item.select('a[href^="/wiki/"]') for item in li if item ]

    result = [ x[0]["href"].replace("/wiki/", "") for x in li if len(x) > 0 ]

  return result

philosophers = []

lists = [ l for l in lists if l != "" ]

for l in lists:
  print "page: %s" % l

  html = get_html(l)

  print "length: %s" % len(html)

  philosophers = philosophers + extract_list(html)

  print

philosophers = list(set(philosophers))
print len(philosophers)
codecs.open("philosophers.txt", "w", "utf-8").write("\n".join(philosophers))
