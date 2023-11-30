from db_connection import connect_db
import json


def init_table(db):
    cursor = db.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS comment
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        competition_id INTEGER,
                        name TEXT,
                        place INTEGER,
                        prise INTEGER
                    )                    
    """)
    db.commit()
    cursor.close()


def parse_data(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def insert_comment_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
                        INSERT INTO comment
                        (
                            competition_id,
                            name,
                            place,
                            prise
                        )
                        VALUES
                        (
                            (SELECT id FROM task1 WHERE name = :name),
                            :name, :place, :prise
                        )
    """, data)
    db.commit()
    cursor.close()


def first_request(db, name):
    """
    Возвращает список словарей с определенным name
    """
    cursor = db.cursor()
    cursor.execute("""
                   SELECT *
                   FROM comment
                   WHERE competition_id = (SELECT id FROM task1 WHERE name = ?)
                   LIMIT 10
    """, [name])
    items = []
    for row in cursor.fetchall():
        row = dict(row)
        items.append(row)
    cursor.close()
    return items


def second_request(db, name):
    """
    Возвращает сумму призовых и количество мест в name
    """
    cursor = db.cursor()
    cursor.execute("""
                    SELECT 
                        SUM(prise) as sum_prises,
                        MAX(place) as max_place
                    FROM comment
                    WHERE competition_id = (SELECT id FROM task1 WHERE name = ?)
                    
    """, [name])
    items = []
    for row in cursor.fetchall():
        row = dict(row)
        items.append(row)

    cursor.close()
    return items


def third_request(db):
    """
    Возвразает список словарей с именем и количеством упоминаний
    """
    cursor = db.cursor()
    data = cursor.execute("""
                    SELECT 
                        name,
                        COUNT(*) as count
                    FROM comment
                    GROUP BY name
    """) 
    items = []
    for row in data.fetchall():
        items.append(dict(row))      
    cursor.close()
    return items


def main():
    conn = connect_db("task1.db")
    init_table(conn)
    #data = parse_data("task_2_var_10_subitem.json")
    #insert_comment_data(conn, data)
    first = first_request(conn, "Сент-Луис 1990")
    print(first)
    second = second_request(conn, "Пальма 2000")
    print(second)
    third = third_request(conn)
    print(third)



if __name__ == "__main__":
    main()