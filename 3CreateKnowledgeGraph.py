import rdflib
import pandas
from rdflib import Graph, Namespace, RDF, RDFS, BNode, Literal
from rdflib.namespace import DC, FOAF, XSD

def create_university(kGraph):
	universityInstance=BNode()
	kGraph.add((universityInstance, RDF.type, universityClass))
	kGraph.add((universityInstance, FOAF.name, Literal("Concordia University",datatype=XSD.string)))
	kGraph.add((universityInstance, DC.source, Literal("http://dbpedia.org/page/Concordia_University",datatype=XSD.string)))
	
	return kGraph, universityInstance

def create_courses(courses, kGraph, universityInstance, courseClass):
	courseIntances_id=dict()
	
	for loop in range(0,len(courses)):
		course=courses[loop]
		
		key=course['Course Subject']+":"+str(course['Course Number'])
		courseInstance=BNode()
		kGraph.add((courseInstance, RDF.type, courseClass))
		kGraph.add((courseInstance, FOAF.name, Literal(course['Course Name'],datatype=XSD.string)))
		kGraph.add((courseInstance, DC.subject, Literal(course['Course Subject'],datatype=XSD.string)))
		kGraph.add((courseInstance, DC.identifier, Literal(course['Course Number'],datatype=XSD.int)))
		kGraph.add((courseInstance, DC.description, Literal(course['Course Description'],datatype=XSD.string)))
		kGraph.add((courseInstance, RDFS.seeAlso, Literal(course['Link'],datatype=XSD.string)))
		kGraph.add((universityInstance, DC.coverage, courseInstance))
		courseIntances_id[key]=courseInstance
	return kGraph, courseIntances_id
	

def create_topics(courseIntances_id, kGraph, topicClass, topics):
	
	
	for loop in range(0,len(topics)):
		topic=topics[loop]
		
		key=topic['Course Subject']+":"+str(topic['Course Number'])
		if key in courseIntances_id:
			topicInstance=BNode()
			kGraph.add((topicInstance, RDF.type, topicClass))
			kGraph.add((topicInstance, FOAF.name, Literal(topic['Topic'],datatype=XSD.string)))
			kGraph.add((topicInstance, DC.subject, Literal(topic['Course Subject'],datatype=XSD.string)))
			kGraph.add((topicInstance, DC.identifier, Literal(topic['Course Number'],datatype=XSD.int)))
			kGraph.add((topicInstance, DC.source, Literal(topic['URI'],datatype=XSD.string)))
			kGraph.add((courseIntances_id[key], DC.hasPart, topicInstance))
	
	return kGraph
	
	
def create_students(kGraph, studentClass, students, universityInstance):
	studentIntances_id=dict()
	
	for loop in range(0,len(students)):
		student=students[loop]
		
		key=str(student['ID Number'])
		studentInstance=BNode()
		kGraph.add((studentInstance, RDF.type, studentClass))
		kGraph.add((studentInstance, FOAF.givenName, Literal(student['FirstName'],datatype=XSD.string)))
		kGraph.add((studentInstance, FOAF.familyName, Literal(student['LastName'],datatype=XSD.string)))
		kGraph.add((studentInstance, DC.identifier, Literal(student['ID Number'],datatype=XSD.int)))
		kGraph.add((studentInstance, FOAF.mbox, Literal(student['Email'],datatype=XSD.string)))
		kGraph.add((studentInstance, FOAF.member, universityInstance))
		studentIntances_id[key]=studentInstance
		
	
	return kGraph, studentIntances_id
	
def create_grades(kGraph, gradeClass, grades, studentIntances_id, DBP, courseIntances_id):
	
	for loop in range(0,len(grades)):
		grade=grades[loop]
		
		keyStudent=str(grade['Student ID'])
		keyCourse=":".join(grade['Course ID(COMP 464)'].split())
		
		if keyStudent in studentIntances_id and keyCourse in courseIntances_id:
			gradeInstance=BNode()
			kGraph.add((gradeInstance, RDF.type, gradeClass))
			kGraph.add((gradeInstance, DC.subject, courseIntances_id[keyCourse]))
			kGraph.add((gradeInstance, DBP.score, Literal(grade['Grade'],datatype=XSD.string)))
			kGraph.add((studentIntances_id[keyStudent], FOAF.topic_interest, gradeInstance))
			
	
	return kGraph
	
	
	
	
kGraph=Graph()
	
DBR=Namespace("http://dbpedia.org/resource/")
DBP=Namespace("http://dbpedia.org/property/")

##CSV files to be created
universitiesCSVname=r"CSV\Universities.csv"
coursesCSVname=r'CSV\Courses.csv'
topicsCSVname=r"CSV\Topics.csv"
studentsCSVname=r"CSV\Students.csv"
gradesCSVname=r"CSV\Grades.csv"

courseClass=DBR.Course
universityClass=DBR.University
topicClass=DBR.Concept
studentClass=DBR.Student
gradeClass=DBR.Grading

courses=pandas.read_csv(coursesCSVname).to_dict('records')
topics=pandas.read_csv(topicsCSVname).to_dict('records')
students=pandas.read_csv(studentsCSVname).to_dict('records')
grades=pandas.read_csv(gradesCSVname).to_dict('records')

kGraph, universityInstance=create_university(kGraph)
kGraph, courseIntances_id=create_courses(courses, kGraph, universityInstance, courseClass)
kGraph=create_topics(courseIntances_id, kGraph, topicClass, topics)
kGraph, studentIntances_id=create_students(kGraph, studentClass, students, universityInstance)
kGraph=create_grades(kGraph, gradeClass, grades, studentIntances_id, DBP, courseIntances_id)
kGraph.serialize(destination='DataGraph.ttl', format='turtle')

	
