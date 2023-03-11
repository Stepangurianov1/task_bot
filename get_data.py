import psycopg2
from settings import PASSWORD, USER, HOST, DBNAME


def get_data(topic, min_difficult, max_difficult):
    conn = psycopg2.connect(dbname=DBNAME, user=USER,
                            password=PASSWORD, host=HOST)
    cursor = conn.cursor()
    cursor.execute(f"SELECT DISTINCT ON (id) id, name, topic,difficult, solved FROM tusks WHERE topic = '{topic}' AND "
                   f"difficult BETWEEN {int(min_difficult)} AND {int(max_difficult)} LIMIT 10")
    data_task = cursor.fetchall()
    cursor.close()
    conn.close()
    return data_task


