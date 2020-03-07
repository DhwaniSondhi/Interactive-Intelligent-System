import spotlight
import pandas

def start():
	universitiesCSVname=r"CSV\Universities.csv"
	coursesCSVname=r'CSV\Courses.csv'
	topicsCSVname=r"CSV\Topics.csv"
	studentsCSVname=r"CSV\Students.csv"
	gradesCSVname=r"CSV\Grades.csv"
	
	courses_df=pandas.read_csv(coursesCSVname)
	courses=courses_df.to_dict('records')
	indexes=list()
	course_topics=list()
	for loop in range(0,50):
		##print(loop, end="")
		try:
			course=courses[loop]
			topic_included=list()
			data=course["Course Name"]+" "+course["Course Description"]
			links=spotlight.annotate('https://api.dbpedia-spotlight.org/en/annotate', course["Course Name"]+" "+course["Course Description"], confidence=0.5, support=20)
			computer_topics=list()	
			for link in links:
				if link['surfaceForm'].lower() not in topic_included:
					topic=dict()
					topic['Course Subject']=course['Course Subject']
					topic['Course Number']=course['Course Number']
					topic_included.append(link['surfaceForm'].lower())
					topic['Topic']=link['surfaceForm']
					topic['URI']=link['URI']
					computer_topics.append(topic)
			
			
			course_topics.extend(computer_topics)
		except:
			indexes.append(loop)
	print("indexes",indexes)
	##to save data
	course_topics_df=pandas.DataFrame(course_topics)
	course_topics_df.to_csv(topicsCSVname)
	
start()
print("done")