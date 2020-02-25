import rdflib
import pandas
from rdflib import Graph, Namespace, RDF, RDFS
from rdflib.namespace import DC, FOAF, XSD
import requests 
from bs4 import BeautifulSoup 

## to add students and course grades:
def generate_students(courses):
	students=list()
	course_grades=list()
	
	names=[('James', 'Smith'),('Michael', 'Smith'),('Robert', 'Smith'),('Maria', 'Garcia'), ('David', 'Smith'), ('Maria', 'Rodriguez'), ('Mary', 'Smith'), ('Maria', 'Hernandez'), ('Maria', 'Martinez'), ('James', 'Johnson')]
	index=0
	id=40083895
	for name in names:
		student=dict()
		
		student['FirstName']=name[0]
		student['LastName']=name[1]
		student['ID Number']=id+index
		student['Email']=name[0].lower()+name[1].lower()+"@gmail.com"
		students.append(student)
		
		grades=['A','B+','A+']
		for loop in range(index+0,index+3):
			if loop<len(courses):
				course_grade=dict()
				course_grade['Student ID']=id+index
				course_grade['Course ID(COMP 464)']=courses[loop]['Course Subject']+" "+courses[loop]['Course Number']
				course_grade['Grade']=grades[loop-index]
				course_grades.append(course_grade)
				
		index+=1	
	return students, course_grades

## to add new links to the base graph
def update_base_graph(baseG, university, course, topic, student, grading, XSD, score_prop):
	baseG.add((university, FOAF.name, XSD.string))
	baseG.add((university, DC.source, XSD.string))
	
	baseG.add((course, FOAF.name, XSD.string))
	baseG.add((course, DC.subject, XSD.string))
	baseG.add((course, DC.identifier, XSD.int))
	baseG.add((course, DC.description, XSD.string))
	baseG.add((course, RDFS.seeAlso, XSD.string))
	
	baseG.add((topic, DC.subject, XSD.string))
	baseG.add((topic, DC.identifier, XSD.int))
	baseG.add((topic, FOAF.name, XSD.string))
	baseG.add((topic, DC.source, XSD.string))
	
	baseG.add((student, FOAF.givenName, XSD.string))
	baseG.add((student, FOAF.familyName, XSD.string))
	baseG.add((student, DC.identifier, XSD.int))
	baseG.add((student, FOAF.mbox, XSD.string))
	
	baseG.add((grading, DC.subject, course))
	baseG.add((grading, score_prop, XSD.string))
	
	baseG.serialize(destination='baseGraph.ttl', format='turtle')
	return baseG
	

## to remove html tags
def clean_data(line):
	line=line.replace("\\n","")
	line=line.replace("&nbsp;"," ")
	line=re.sub(r'(?is)<[^>]*>', '', line)
	line=line.split()
	if not (len(line)>2 and len(line[0])==4 and line[1].isdigit()):
		line=[]
	return line

## to get courses and save them in a CSV(coursesCSVname)
def get_courses(url, coursesCSVname, course_subs):
	check_credit='credits)'
	page=requests.get(url)
	bSoup = BeautifulSoup(page.content, 'html5lib') 
	req_spans = bSoup.find_all('span', {'class' : 'large-text'})
	
	spandata=list()
	for span in req_spans:
		spandata.extend(span.getText().splitlines())
	
	for loop in range(0,len(spandata)):
		base_loop=loop
		line=spandata[loop]
		index=line.find(check_credit)
		if index>0:
			key=line.split()[0]+":"+line.split()[1]
			description=""
			enter=False
			loop+=1
			while(loop<len(spandata) and spandata[loop].find(check_credit)<0):
				description+=spandata[loop]
				enter=True
				loop+=1
			
			loop-=1
			spandata[base_loop]+=description
			
	description_dict=dict()
	for line in spandata:
		index=line.find(check_credit)
		if index>0:
			desp=line[index+len(check_credit):]
			if len(desp.strip())>0:
				key=line.split()[0]+":"+line.split()[1]
				description_dict[key]=desp
				
			
	courses=list()
	courses_done=list()
	for line in spandata:
		line_arr=line.split()
		key=line_arr[0]+":"+line_arr[1]
		if line_arr[0] in course_subs  and  line_arr[1].isdigit() and key not in courses_done:
			courses_done.append(key)
			course=dict()
			if line.find(check_credit)>0:
				startindex=line.find(line_arr[2])
				course["Course Name"]=line[startindex:line.find(check_credit)+len(check_credit)]
			else:
				course["Course Name"]=" ".join(line_arr[2:])
			course["Course Subject"]=line_arr[0]
			course["Course Number"]=line_arr[1]
			course["Course Description"]=""
			key=course["Course Subject"]+":"+course["Course Number"]
			if key in description_dict:
				course["Course Description"]=description_dict[key]
			course["Link"]=""
			courses.append(course)
	
	return courses
	
def start(baseGname, urls, course_subs):
	baseG = rdflib.Graph()
	baseG.parse(baseGname, format="ttl")

	##CSV files to be created
	universitiesCSVname=r"CSV\Universities.csv"
	coursesCSVname=r'CSV\Courses.csv'
	topicsCSVname=r"CSV\Topics.csv"
	studentsCSVname=r"CSV\Students.csv"
	gradesCSVname=r"CSV\Grades.csv"

	##Updating base graph
	dbr=Namespace("http://dbpedia.org/resource/")
	dbp=Namespace("http://dbpedia.org/property/")
	baseG=update_base_graph(baseG, dbr.University, dbr.Course, dbr.Concept, dbr.Student, dbr.Grading, XSD, dbp.score)

	##to get courses and create Courses CSV
	courses=list()
	for url in urls:
		in_courses=get_courses(url, coursesCSVname, course_subs)
		#print(len(in_courses))
		courses.extend(in_courses)
		
		
	##to save courses
	courses_df=pandas.DataFrame(courses)
	courses_df.to_csv(coursesCSVname)
	
	## courses only taken 10 for now
	students, course_grades=generate_students(courses[:10])
	##to save students
	students_df=pandas.DataFrame(students)
	students_df.to_csv(studentsCSVname)
	
	##to save course and grades
	course_grades_df=pandas.DataFrame(course_grades)
	course_grades_df.to_csv(gradesCSVname)

urls=["https://www.concordia.ca/academics/graduate/calendar/current/encs/computer-science-courses.html",
	"https://www.concordia.ca/academics/graduate/calendar/current/encs/engineering-courses.html"]
course_subs=["ENCS","ENGR","BLDG", "COEN", "CIVI", "ELEC", "INDU", "MECH", "INSE", "CHME", "MBA", "BCEE", "COMP","SOEN"]
baseGname="base.ttl"
start(baseGname, urls, course_subs)