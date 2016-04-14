# coding: utf-8

import json
import codecs
import mpi4py
import pandas as pd
import networkx as nx

from gensim import corpora, models

def get_sentences(doc_name):
  sentences = []
  # sentences = models.word2vec.LineSentence("datasets/sentences/%s.txt" % doc_name.replace("/", "-"))
  sentences = codecs.open("../datasets/sentences/%s.txt" % doc_name.replace("/", "-"),"r", "utf-8").read().split("\n")
  sentences = [ s.split() for s in sentences ]

  return sentences

G = nx.read_gexf("../datasets/influences.gexf")
names = G.nodes()
sentences = reduce(lambda a,b: a + b, map(get_sentences, names))

bigram = models.phrases.Phrases(sentences)
dictionary = corpora.Dictionary(bigram[sentences])
corpus = [ dictionary.doc2bow(text) for text in bigram[sentences] ]

model = models.ldamodel.LdaMulticore(corpus=corpus, workers=9, id2word=dictionary, num_topics=100, alpha=0, chunksize=1000, update_every=1)

model.save("../../tmp/100topics.txt")
