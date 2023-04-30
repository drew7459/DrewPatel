from neo4j import GraphDatabase, basic_auth

uri = "bolt://localhost:7687"
user = "neo4j"
password = "test_root"
database = "academicworld"
driver = GraphDatabase.driver(uri, auth=basic_auth(user, password), database=database)

query = """
MATCH (f:FACULTY)-[:AFFILIATION_WITH]->(i:INSTITUTE)
WHERE i.name = 'University of illinois at Urbana Champaign'
MATCH (f)-[:PUBLISH]->(p:PUBLICATION)-[lb:LABEL_BY]->(kw:KEYWORD)
WHERE kw.name = 'machine learning'
RETURN f.name AS facultyName, sum(p.numCitations * lb.score) AS KRC
ORDER BY KRC DESC
LIMIT 10
"""

def getFaculty():
    result = []
    with driver.session() as session:
        records = session.run(query)
        for record in records:
            result.append({
                'Faculty Name': record['facultyName'],
                'KRC': record['KRC']
            })
    print(result)
    driver.close()
    return result

"""
Find the faculty member who is ranked highest by the keyword-relevant citation to “machine learning”.

Query: 
MATCH (f:FACULTY)-[:AFFILIATION_WITH]->(i:INSTITUTE)
WHERE i.name = 'University of illinois at Urbana Champaign'
MATCH (f)-[:PUBLISH]->(p:PUBLICATION)-[lb:LABEL_BY]->(kw:KEYWORD)
WHERE kw.name = 'machine learning'
RETURN f.name AS facultyName, sum(p.numCitations * lb.score) AS KRC
ORDER BY KRC DESC
LIMIT 10

Find the top-10 popular keywords by the number of faculty members who are interested in them. 
A faculty member is interested in a keyword if there is a “INTERESTED_IN”relationship between them. 
Return the keywords and number of faculty members.

MATCH (f:FACULTY)-[:INTERESTED_IN]->(k:KEYWORD)
WITH k, COUNT(f) as faculty_count
RETURN k.name as keyword, faculty_count
ORDER BY faculty_count DESC
LIMIT 10
"""
