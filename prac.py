import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF


g = rdflib.Graph()
g.parse("new.ttl", format="ttl")

bob = URIRef("http://example.org/people/Bob")
g.add((bob, FOAF.Name, FOAF.Literal))

for subj, pred, obj in g:
	print(subj, pred, obj)