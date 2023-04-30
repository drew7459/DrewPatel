import pymysql

db = pymysql.connect(host='localhost',
                user='root',
                password='test_root',
                database='academicworld',
                charset='utf8mb4',
                port=3306,
                cursorclass=pymysql.cursors.DictCursor)

def get_university(input_value):
    with db.cursor() as cursor:
        sql = 'select id, name from university where name like "%' + input_value + '%";'
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

def get_faculty_counts():
    query = """
    SELECT u.name, COUNT(DISTINCT f.id) AS num_faculty
    FROM university u
    JOIN faculty f ON u.id = f.university_id
    JOIN faculty_keyword fk ON f.id = fk.faculty_id
    JOIN keyword k ON fk.keyword_id = k.id
    WHERE k.name LIKE '%data%'
    GROUP BY u.id, u.name
    ORDER BY num_faculty DESC
    LIMIT 10;
    """

    with db.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return result

def get_topFaculty():
    query = """
    SELECT f.name, SUM(pk.score * p.num_citations) AS KRC
    FROM faculty f
    JOIN faculty_publication fp ON f.id = fp.faculty_id
    JOIN publication p ON fp.publication_id = p.id
    JOIN publication_keyword pk ON p.id = pk.publication_id
    JOIN keyword k ON pk.keyword_id = k.id
    WHERE k.name = 'data'
    GROUP BY f.id, f.name
    ORDER BY KRC DESC
    LIMIT 10;
    """

    with db.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return result

def get_faculty_publications(faculty_name):
    query = f"""
    SELECT publication.title, publication.year, publication.num_citations
    FROM publication
    JOIN faculty_publication ON publication.id = faculty_publication.publication_id
    JOIN faculty ON faculty.id = faculty_publication.faculty_id
    WHERE faculty.name = '{faculty_name}'
    ORDER BY publication.num_citations DESC;
    """

    with db.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return result

def get_favorites():
    query = "SELECT name, email FROM faculty WHERE favorite = 1 ORDER BY name ASC;"

    with db.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        return result

def getFaculty():
    query = "SELECT name, position, email, phone, favorite FROM faculty;"
    with db.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return result

def add_favorite(name):
    query = "UPDATE faculty SET favorite = 1 WHERE name = %s"
    with db.cursor() as cursor:
        cursor.execute(query, (name,))
        db.commit()

def delete_favorite(name):
    query = "DELETE FROM favorites WHERE name = %s"
    print("delete call")
    with db.cursor() as cursor:
        cursor.execute(query, (name,))
        db.commit()