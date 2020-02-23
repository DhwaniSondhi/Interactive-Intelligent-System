import rdflib
import pandas
import sys
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, RDFS
from rdflib.namespace import DC, FOAF


def update_base_graph(baseG, university, course, topic, student):
	baseG.add((university, FOAF.name, xsd.string))
	baseG.add((university, RDFS.seeAlso, xsd.string))
	
	baseG.add((course, FOAF.name, xsd.string))
	baseG.add((course, DC.subject, xsd.string))
	baseG.add((course, DC.identifier, xsd.int))
	baseG.add((course, DC.description, xsd.string))
	baseG.add((course, RDFS.seeAlso, xsd.string))
	
	baseG.add((topic, FOAF.name, xsd.string))
	baseG.add((topic, DC.description, xsd.string))
	baseG.add((topic, RDFS.seeAlso, xsd.string))
	
	baseG.add((student, FOAF.givenName, xsd.string))
	baseG.add((student, FOAF.familyName, xsd.string))
	baseG.add((student, DC.identifier, xsd.int))
	baseG.add((student, FOAF.mbox, xsd.string))
	
	baseG.serialize(destination='baseGraph.txt', format='turtle')
	return baseG
	

baseG = rdflib.Graph()
baseG.parse("base.ttl", format="ttl")

universities=pandas.read_csv("CSV/Universities.csv")
courses=pandas.read_csv("CSV/Courses.csv")
topics=pandas.read_csv("CSV/Topics.csv")
students=pandas.read_csv("CSV/Students.csv")
grades=pandas.read_csv("CSV/Grades.csv")

##Updating base graph
xsd=Namespace("http://www.w3.org/2001/XMLSchema#")
dbr=Namespace("http://dbpedia.org/resource/")
university=dbr.University
course=dbr.Course
topic=dbr.Concept
student=dbr.Student
baseG=update_base_graph(baseG, university, course, topic, student)

for subj, pred, obj in baseG:
	print(subj, pred, obj)