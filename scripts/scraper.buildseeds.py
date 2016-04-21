#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import codecs

from bs4 import BeautifulSoup

from wekeypedia import WikipediaPage as page

lists = [
  u"Lists_of_philosophers"
]

def get_html(name):
  p = page(name, "en")
  content = p.get_current()

  return content

def extract_list(html):
  soup = BeautifulSoup(html, "html.parser")

  result = []

  li = reduce(lambda a,b: a+b, [ ul.find_all("li") for ul in soup.select("h2 + ul") ])

  li = [ item.select('a[href^="/wiki/"]') for item in li if item ]

  result = [ x[0]["href"].replace("/wiki/", "") for x in li if len(x) > 0 ]

  return result

seeds = []

for l in lists:
  print "page: %s" % l

  html = get_html(l)

  print "length: %s" % len(html)

  seeds = seeds + extract_list(html)

  print

seeds = list(set(seeds))
print len(seeds)
codecs.open("../datasets/seeds.txt", "w", "utf-8").write("\n".join(seeds))
