## Interactive Intelligent System
 This is a combination of two assignments of COMP6741 Intelligent Systems. These assignments aimed to develop an intelligent agent that can answer University-related questions by creating a Knowledge-graph using Web Scraping and converting questions using Regular Expressions. 
 
### Basics:
- **Knowledge Graphs** are information represented in the form of graphs.
- **Nodes** are the entities and **Edges** are the relationships between nodes.
- Each fact in the knowledge graph is represented as a **triple (subject, predicate, object)**.

### Project Introduction:
- Our knowledge graph stores information about all the undergraduate and graduate courses at Concordia University.
- The courses are being linked to topics covered and dummy students with grades. 
- The answers to the queries are given using SPARQL queries.
- Knowledge graph is extracted using web scraping of Concordia website's pages.
- Graphs are based on turtle format.
- Used Regular Expressions to translate given input into SPARQL queries.

### DataSet Created:
- **Courses.csv** stores the data related to courses and their properties.
- **Grades.csv** stores the courses and the grade scores by each student.
- **Student.csv** stores information about students such as name, email, id, etc.
- **Topics.csv** stores information and DBpedia links for Topics for each course.
- **Universities.csv** stores information about universities and their DBpedia entries.

### How to run?
- Set up an environment and install Pandas, Rdflib, Spotlight, and BeautifulSoup.
- Run 1LoadCoursesStudentsGrades.py which takes input from the “universityKG.ttl” file and saves the data in the respective files in the CSV folder.
- Run 2LoadLinkTopics.py which takes input from the Courses.csv and saves the data in respective files in the CSV folder.
- Run 3CreateKnowledgeGraph.py which takes input from the “universityKG.ttl” file and the files in the CSV folder and saves the triplets in “DataGraph.ttl”. Steps 1-3 creates the Knowledge Graph.
- Run 4RunQueries.py to ask test SPARQL queries to the knowledge base if needed.
- Run 5Chatbot.py to ask questions from the Chatbot.

[Please click for the output images](https://github.com/DhwaniSondhi/Interactive-Intelligent-System/tree/master/output%20images)<br/>
[Please click for the complete report](https://github.com/DhwaniSondhi/Interactive-Intelligent-System/blob/master/Report.pdf)
