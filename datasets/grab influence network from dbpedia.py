
# coding: utf-8

# In[1]:

from SPARQLWrapper import SPARQLWrapper, JSON


# In[5]:

endpoint = "http://dbpedia.org/sparql"

query = """
PREFIX dbo: <http://dbpedia.org/ontology/>

CONSTRUCT {
  ?s dbo:influencedBy ?t1.
  ?s dbo:influenced ?t2.
}
where { 
  ?s rdf:type dbo:Philosopher.

  OPTIONAL { ?s dbo:influencedBy ?t1. ?t1 rdf:type dbo:Person. }
  OPTIONAL { ?s dbo:influenced ?t2. ?t2 rdf:type dbo:Person. }
}
"""

sparql = SPARQLWrapper(endpoint)
sparql.setQuery(query)
sparql.setReturnFormat(JSON)

results = sparql.query().convert()

print len(results)


# In[7]:

print len(results["results"]["bindings"])


# In[9]:

import json

with open('influences.dbpedia.json', 'w') as outfile:
    json.dump(results["results"]["bindings"], outfile)

