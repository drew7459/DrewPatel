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
