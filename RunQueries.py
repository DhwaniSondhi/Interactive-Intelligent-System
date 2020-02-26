import rdflib
g=rdflib.Graph()
g.parse("baseGraph.ttl", format='turtle')
g.parse("DataGraph.ttl", format='turtle')

prefix="""PREFIX dbr: <http://dbpedia.org/resource/>
prefix dbp: <http://dbpedia.org/property/> 
prefix dbr: <http://dbpedia.org/resource/> 
prefix dc: <http://purl.org/dc/elements/1.1/> 
prefix foaf: <http://xmlns.com/foaf/0.1/> 
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
"""
query1=prefix+"""
SELECT (COUNT(*) as ?Triples) 
WHERE { 
?s ?p ?o
}
"""
query2=prefix+"""
SELECT  
(COUNT(DISTINCT ?students) as ?scount)
(COUNT(DISTINCT ?courses) as ?ccount)
(COUNT(DISTINCT ?t) as ?tcount)
WHERE{

  ?students rdf:type dbr:Student .
  ?courses rdf:type dbr:Course .
  ?k dc:hasPart ?x.
  ?x foaf:name ?t.
 }
"""
 
query3=prefix+"""
SELECT ?topic ?dbentry
WHERE{
 ?course rdf:type dbr:Course .
 ?course foaf:name ?name .
 ?course foaf:name "Machine Learning"^^xsd:string.
 ?course dc:hasPart ?x.
 ?x foaf:name ?topic .
 ?x dc:source ?dbentry
 }
"""
query4=prefix+"""
SELECT ?fn ?score ?coursename
WHERE { 
 ?s rdf:type dbr:Student;
 foaf:familyName ?ln;
 foaf:givenName ?fn ;
 dc:identifier "40083896"^^xsd:int.
 ?s foaf:topic_interest ?gradeobject .
 ?gradeobject   dbp:score ?score ;
 dc:subject ?courseobject .
 ?courseobject foaf:name ?coursename
}
"""
query5=prefix+"""
                  
SELECT ?fn ?coursename ?grade ?topicname
WHERE { 
?s rdf:type dbr:Student;
 foaf:familyName ?ln;
 foaf:givenName ?fn ;
 dc:identifier ?e.
 ?s foaf:topic_interest ?gradeobject.
 ?gradeobject dc:subject  ?courseobject .
 ?gradeobject dbp:score ?grade .
  ?courseobject foaf:name ?coursename.
  ?courseobject dc:hasPart ?topic.
  ?topic foaf:name ?topicname.
  ?topic foaf:name "CORBA"^^xsd:string.
  FILTER(?grade <"F")
} 
"""
query6=prefix+"""
                  
SELECT DISTINCT ?fn ?topicname ?coursename ?grade 
WHERE { 
?s rdf:type dbr:Student;
 foaf:familyName ?ln;
 foaf:givenName ?fn ;
 foaf:givenName "Michael"^^xsd:string ;
 foaf:mbox ?mb;
 dc:identifier ?e.
 ?s foaf:topic_interest ?gradeobject.
 ?gradeobject dc:subject  ?courseobject .
 ?gradeobject dbp:score ?grade .
  ?courseobject foaf:name ?coursename.
  ?courseobject dc:hasPart ?topic.
  ?topic foaf:name ?topicname.
  FILTER(?grade <"F")
}  
 
"""
print("\n\n-------------------------------------------------------------------\n")
print("\n\n1. Total number of triples in the KB\n")
for row in g.query(query1):
   print() 
   for c in row:
        print("Total no of triples:",c,)
    
print("\n\n-------------------------------------------------------------------\n")
print("\n\n2. Total number of students, courses, and topics")
print("Students  Courses  Topics")
for row in g.query(query2):
   for c in row:
        print(c,end=", ")
    
print("\n\n-------------------------------------------------------------------\n")
print("\n\n3. For a course c, list all covered topics using their (English) labels and their link to DBpedia\n")
res=g.query(query3)
for row in res:
   for c in row:
        print(c, end=": ")
    
print("\n\n-------------------------------------------------------------------\n")
print("\n\n4. For a given student, list all courses this student completed, together with the grade\n")
print("Name  Grade  Course", end="")
for row in g.query(query4):
   print() 
   for c in row:
        print(c,end=", ")
    
print("\n\n-------------------------------------------------------------------\n")
print("\n\n5. For a given topic, list all students that are familiar with the topic")
print("Name | Course | Grade | Topic", end="")
for row in g.query(query5):
   print() 
   for c in row:
        print(c,end=", ")
print("\n\n-------------------------------------------------------------------\n")
print("\n\n6.For a student, list all topics (no duplicates) that this student is familiar with")
print(" Name | Topic | Course | Grade ", end="")
for row in g.query(query6):
   print() 
   for c in row:
        print(c,end=", ")
print("\n\n-------------------------------------------------------------------\n")