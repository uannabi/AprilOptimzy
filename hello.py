import fire
from rdflib.graph import Graph

def hello(name="World"):
  g = Graph()
  g.parse("demo.nt", format="nt")
  return "Hello %s!" % name

if __name__ == '__main__':
  fire.Fire(hello)
