
# coding: utf-8

# In[9]:

import os.path
import codecs
import networkx as nx
from wekeypedia import WikipediaPage as page


# In[2]:

G = nx.read_gexf("influences.gexf")


# In[3]:

names = list(set(G.nodes()))

print len(names)


# In[18]:

def grab_and_save(name):
  if os.path.exists("pages/%s.html" % name):
    return
    #pass

  print name


  try:
    p = page(name, "en")
    content = p.get_current()
  except:
    content = ""
  
  f = codecs.open("pages/%s.html" % name, "w", "utf-8")
  f.write(content)
  f.close()
  
for name in names[0:10]:
  grab_and_save(name)
  
print "done"


# ## multithreaded grabbing

# In[ ]:

from multiprocessing import Pool as ThreadPool

pool = ThreadPool(4)

pool.map(grab_and_save, names)

pool.close()
pool.join()

print "done"

