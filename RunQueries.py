import rdflib
g=rdflib.Graph()
g.parse("baseGraph.ttl", format='turtle')
g.parse("DataGraph.ttl", format='turtle')

starter="""PREFIX dbr: <http://dbpedia.org/resource/>
prefix dbp: <http://dbpedia.org/property/> 
prefix dbr: <http://dbpedia.org/resource/> 
prefix dc: <http://purl.org/dc/elements/1.1/> 
prefix foaf: <http://xmlns.com/foaf/0.1/> 
prefix isp: <http://intelligentsystemproj1.io/schema#> 
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
prefix xml: <http://www.w3.org/XML/1998/namespace> 
prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
"""
query1=starter+"""
SELECT (COUNT(*) as ?Triples) 
WHERE { 
?s ?p ?o
}
"""
query2=starter+"""
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
query3=starter+"""
SELECT ?topic 
WHERE{
?course rdf:type dbr:Course .
?course foaf:name ?name .
?course foaf:name "Machine Learning"^^xsd:string.
?course dc:hasPart ?x.
?x foaf:name ?topic
 }
"""
query4=starter+"""
SELECT ?fn ?score ?coursename
WHERE { 
?s rdf:type dbr:Student;
 foaf:familyName ?ln;
 foaf:givenName ?fn ;
 foaf:mbox ?mb;
 dc:identifier "40083896"^^xsd:int.
?s foaf:topic_interest ?gradeobject .
?gradeobject   dbp:score ?score ;
    dc:subject ?courseobject .
?courseobject foaf:name ?coursename
}
"""
query5=starter+"""
                  
SELECT ?fn ?coursename ?grade ?topicname
WHERE { 
?s rdf:type dbr:Student;
 foaf:familyName ?ln;
 foaf:givenName ?fn ;
 foaf:mbox ?mb;
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
query6=starter+"""
                  
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
print("\n\nQ1.Count the no of triples.\n")
for row in g.query(query1):
   for c in row:
        print("Total no of triples:",c,end=" ")
    
print("\n\nQ2.Count the number of students, courses, topics")
print("Students  Courses  Topics")
for row in g.query(query2):
   for c in row:
        print(c,end=" ")
    
print("\n\nQ3.For a course c, list all covered topics using their (English) labels and their link to DBpedia\n")
res=g.query(query3)
for row in res:
   for c in row:
        print(c)
    
print("\n\nQ4. For a given student, list all courses this student completed, together with the grade.\n")
print("Name  Grade  Course", end="")
for row in g.query(query4):
   print() 
   for c in row:
        print(c,end=" ")
    
print("\n\nQ5.For a given topic, list all students that are familiar with the topic (i.e., took, and did not fail, acourse that covered the topic)")
print("Name | Course | Grade | Topic", end="")
for row in g.query(query5):
   print() 
   for c in row:
        print(c,end=" ")
print("\n\nQ6. For a student, list all topics (no duplicates) that this student is familiar with (based on the completedcourses for this student that are better than an \F grade")
print(" Name | Topic | Course | Grade ", end="")
for row in g.query(query6):
   print() 
   for c in row:
        print(c,end=" ")